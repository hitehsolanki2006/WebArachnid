# 🕸️ WebArachnid CLI — Target Analysis Toolkit

**WebArachnid CLI** is a modular, open-source cybersecurity tool built for OSINT, reconnaissance, scanning, and offensive analysis of web targets. It combines the power of Linux tools with the flexibility of Python.

> 🎯 Perfect for bug bounty hunters, red teamers, and cybersecurity learners.

---

## 🚀 Features

| Module             | Purpose                                              | Tools Used                          |
|--------------------|------------------------------------------------------|-------------------------------------|
| `whois`            | Domain info & registrar details                      | `whois`                             |
| `dns`              | DNS records, zone transfer check                     | `dig`                               |
| `ports`            | TCP/UDP port scan + service detection                | `nmap`                              |
| `fingerprint`      | Web tech detection, CMS, server banners              | `whatweb`                           |
| `direnum`          | Directory and file bruteforce                        | `ffuf`                              |
| `vulnscan`         | CVE scans, server issues, OWASP findings             | `nikto`, `nuclei`                   |
| *(more coming)*    |                                                      |                                     |

---

## 🛠️ Requirements

Make sure these tools are installed:

```bash
sudo apt install whois dig nmap whatweb ffuf nikto nuclei
