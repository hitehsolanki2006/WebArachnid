# core/recon/port_scan.py

import subprocess
import os
import re

def run(target):
    print(f"[+] Running Nmap port scan on {target}")
    try:
        os.makedirs("output", exist_ok=True)
        output_file = f"output/ports_{target.replace('.', '_')}.txt"

        # -Pn = skip ping
        # -sV = version detection
        # -O  = OS detection
        print("[*] Scanning... this may take a moment.")
        result = subprocess.run(
            ['nmap', '-Pn', '-sV', '-O', target],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"[!] Nmap error:\n{result.stderr}")
            return

        raw_output = result.stdout

        # Save raw nmap result
        with open(output_file, 'w') as f:
            f.write(raw_output)

        print("\n" + "="*60)
        print("[ Nmap Summary ]")
        print("="*60)

        # Simple extraction of open ports & services
        open_ports = re.findall(r'^(\d+/tcp|\d+/udp)\s+open\s+(\S+)\s+(.*)', raw_output, re.MULTILINE)
        if not open_ports:
            print("No open ports found.")
        else:
            for port, service, version in open_ports:
                print(f"{port:8} | {service:12} | {version}")

        print(f"\n[✓] Full Nmap report saved to: {output_file}")

    except Exception as e:
        print(f"[!] Port scan failed: {e}")
