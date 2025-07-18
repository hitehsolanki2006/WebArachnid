# core/recon/dns_enum.py

import subprocess
import os

def dig_record(target, record_type):
    try:
        result = subprocess.run(['dig', '+short', target, record_type], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error running dig {record_type}: {e}"

def run(target):
    print(f"[+] Running DNS Enumeration for {target}")
    try:
        os.makedirs("output", exist_ok=True)
        output_path = f"output/dns_{target.replace('.', '_')}.txt"
        with open(output_path, 'w') as f:

            def log(title, data):
                print(f"\n--- {title} ---")
                print(data if data else "No data found.")
                f.write(f"=== {title} ===\n{data if data else 'No data'}\n\n")

            log("A Records", dig_record(target, 'A'))
            log("NS Records", dig_record(target, 'NS'))
            log("MX Records", dig_record(target, 'MX'))
            log("TXT Records", dig_record(target, 'TXT'))

            # Zone Transfer Check (AXFR)
            zone_transfer = subprocess.run(['dig', '@' + target, target, 'AXFR'], capture_output=True, text=True)
            if "Transfer failed" in zone_transfer.stdout or zone_transfer.returncode != 0:
                log("Zone Transfer", "Zone transfer failed or not allowed.")
            else:
                log("Zone Transfer", zone_transfer.stdout.strip())

        print(f"\n[✓] DNS info saved to: {output_path}")

    except Exception as e:
        print(f"[!] DNS Enumeration Error: {e}")
