#!/usr/bin/env python3
"""
Port Scanner Simples
=====================
Um scanner de portas TCP multithreaded com detecção básica de serviço
e saída colorida no terminal.

Uso educacional. Escaneie apenas hosts que você tem permissão de testar.
"""

import argparse
import socket
import sys
import threading
import queue
import time
from datetime import datetime


# ----------------------------
# Cores ANSI para terminal
# ----------------------------
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# Mapeamento simples de portas conhecidas -> serviço
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    111: "RPCBind",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}


def grab_banner(sock):
    """Tenta capturar o banner de serviço, se disponível."""
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner if banner else None
    except Exception:
        return None


def scan_port(target, port, timeout, results, results_lock, grab_banners):
    """Escaneia uma única porta TCP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "unknown")
                banner = grab_banner(sock) if grab_banners else None
                with results_lock:
                    results.append((port, service, banner))
    except socket.error:
        pass


def worker(target, port_queue, timeout, results, results_lock, grab_banners):
    while True:
        try:
            port = port_queue.get_nowait()
        except queue.Empty:
            return
        scan_port(target, port, timeout, results, results_lock, grab_banners)
        port_queue.task_done()


def resolve_target(target):
    """Resolve hostname para IP. Retorna None se falhar."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def parse_ports(port_range):
    """Converte string tipo '1-1000' ou '22,80,443' em lista de portas."""
    ports = set()
    for part in port_range.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def print_banner():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 55)
    print("           PORT SCANNER SIMPLES - by nyvrex")
    print("=" * 55)
    print(f"{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Scanner de portas TCP simples com threading e detecção de serviço."
    )
    parser.add_argument("target", help="IP ou hostname alvo")
    parser.add_argument(
        "-p", "--ports", default="1-1024",
        help="Portas a escanear. Ex: 22,80,443 ou 1-1000 (padrão: 1-1024)"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=100,
        help="Número de threads (padrão: 100)"
    )
    parser.add_argument(
        "--timeout", type=float, default=0.5,
        help="Timeout de conexão em segundos (padrão: 0.5)"
    )
    parser.add_argument(
        "-b", "--banner", action="store_true",
        help="Tentar capturar banner de serviço"
    )

    args = parser.parse_args()

    print_banner()

    target_ip = resolve_target(args.target)
    if not target_ip:
        print(f"{Colors.RED}[!] Não foi possível resolver o host: {args.target}{Colors.RESET}")
        sys.exit(1)

    try:
        ports = parse_ports(args.ports)
    except ValueError:
        print(f"{Colors.RED}[!] Formato de portas inválido: {args.ports}{Colors.RESET}")
        sys.exit(1)

    print(f"{Colors.YELLOW}[*] Alvo:{Colors.RESET} {args.target} ({target_ip})")
    print(f"{Colors.YELLOW}[*] Portas:{Colors.RESET} {len(ports)} portas")
    print(f"{Colors.YELLOW}[*] Threads:{Colors.RESET} {args.threads}")
    print(f"{Colors.YELLOW}[*] Início:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    port_queue = queue.Queue()
    for port in ports:
        port_queue.put(port)

    results = []
    results_lock = threading.Lock()

    start_time = time.time()

    threads = []
    for _ in range(min(args.threads, len(ports))):
        t = threading.Thread(
            target=worker,
            args=(target_ip, port_queue, args.timeout, results, results_lock, args.banner),
            daemon=True,
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    elapsed = time.time() - start_time

    results.sort(key=lambda x: x[0])

    if results:
        print(f"{Colors.GREEN}{Colors.BOLD}PORT       STATE      SERVICE{Colors.RESET}")
        print("-" * 45)
        for port, service, banner in results:
            line = f"{Colors.GREEN}{str(port) + '/tcp':<11}open       {service}{Colors.RESET}"
            print(line)
            if banner:
                print(f"{Colors.CYAN}           └─ banner: {banner[:60]}{Colors.RESET}")
    else:
        print(f"{Colors.RED}[!] Nenhuma porta aberta encontrada.{Colors.RESET}")

    print(f"\n{Colors.YELLOW}[*] Scan finalizado em {elapsed:.2f} segundos "
          f"({len(results)} porta(s) aberta(s)){Colors.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Scan interrompido pelo usuário.{Colors.RESET}")
        sys.exit(0)
