# 🔍 Port Scanner Simples

Um scanner de portas TCP em Python, com **multithreading**, **saída colorida** no terminal e **detecção básica de serviço**.

Projeto criado para fins de estudo e prática de redes/segurança ofensiva.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Funcionalidades

- Escaneamento de portas TCP com múltiplas threads (rápido)
- Suporte a range de portas (`1-1000`) ou lista específica (`22,80,443`)
- Identificação de serviços comuns (SSH, HTTP, MySQL, RDP, etc.)
- Captura opcional de banner de serviço
- Saída colorida e organizada no terminal
- Resolução automática de hostname → IP

---

## 📦 Instalação

```bash
git clone https://github.com/nyvrex/swiftscan.git
cd swiftscan
```

Não há dependências externas — usa apenas a biblioteca padrão do Python 3.

---

## 🚀 Uso

```bash
python3 scanner.py <alvo> [opções]
```

### Exemplos

Escanear as 1024 portas mais comuns:
```bash
python3 scanner.py 192.168.1.1
```

Escanear um range específico:
```bash
python3 scanner.py scanme.nmap.org -p 1-500
```

Escanear portas específicas com captura de banner:
```bash
python3 scanner.py 192.168.1.1 -p 22,80,443 -b
```

Ajustar threads e timeout:
```bash
python3 scanner.py 10.0.0.5 -p 1-65535 -t 200 --timeout 0.3
```

### Opções

| Flag | Descrição | Padrão |
|------|-----------|--------|
| `-p`, `--ports` | Portas a escanear (range ou lista) | `1-1024` |
| `-t`, `--threads` | Número de threads simultâneas | `100` |
| `--timeout` | Timeout de conexão (segundos) | `0.5` |
| `-b`, `--banner` | Tentar capturar banner do serviço | desativado |

---

## 📸 Exemplo de saída

```
=======================================================
           PORT SCANNER SIMPLES - by nyvrex
=======================================================

[*] Alvo: scanme.nmap.org (45.33.32.156)
[*] Portas: 1024 portas
[*] Threads: 100
[*] Início: 2026-08-16 21:40:00

PORT       STATE      SERVICE
---------------------------------------------
22/tcp     open       SSH
80/tcp     open       HTTP

[*] Scan finalizado em 3.42 segundos (2 porta(s) aberta(s))
```

---

## ⚠️ Aviso legal

Esta ferramenta é destinada **exclusivamente a fins educacionais** e para testes em ambientes onde você tem **autorização explícita**. Escanear redes ou hosts sem permissão pode violar leis locais e internacionais (ex: Lei Carolina Dieckmann, Computer Fraud and Abuse Act). O autor não se responsabiliza por uso indevido.

Use com responsabilidade. Ambientes recomendados para prática:
- [scanme.nmap.org](http://scanme.nmap.org) (alvo oficial de teste do Nmap)
- Máquinas virtuais próprias (ex: Metasploitable)
- Labs como TryHackMe / HackTheBox

---

## 🛠️ Possíveis melhorias futuras

- [ ] Suporte a escaneamento UDP
- [ ] Exportar resultados em JSON/CSV
- [ ] Detecção de SO (fingerprinting)
- [ ] Modo silencioso (`--quiet`) para scripts
- [ ] Barra de progresso

---

## 📄 Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.
