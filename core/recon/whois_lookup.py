# core/recon/whois_lookup.py

import subprocess
import os
import re

def run(target):
    print(f"[+] Running WHOIS lookup for {target}")
    try:
        os.makedirs("output", exist_ok=True)
        result = subprocess.run(['whois', target], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[!] WHOIS command failed:\n{result.stderr}")
            return

        raw_output = result.stdout

        # Save full raw WHOIS to file
        output_path = f"output/whois_{target.replace('.', '_')}.txt"
        with open(output_path, 'w') as f:
            f.write(raw_output)

        # Extract key details using regex
        def extract(label, pattern, multi=False):
            matches = re.findall(pattern, raw_output, re.IGNORECASE)
            if multi:
                return ', '.join(set(m.strip() for m in matches))
            return matches[0].strip() if matches else 'N/A'

        summary = {
            "Domain Name": extract("Domain Name", r"Domain Name:\s+([^\n]+)"),
            "Registrar": extract("Registrar", r"Registrar:\s+([^\n]+)"),
            "Creation Date": extract("Creation Date", r"Creation Date:\s+([^\nT]+)"),
            "Expiration Date": extract("Expiration Date", r"(?:Registry Expiry Date|Registrar Registration Expiration Date):\s+([^\nT]+)"),
            "Updated Date": extract("Updated Date", r"Updated Date:\s+([^\nT]+)"),
            "Domain Status": extract("Domain Status", r"Domain Status:\s+([^\n]+)", multi=True),
            "Name Servers": extract("Name Server", r"Name Server:\s+([^\n]+)", multi=True),
            "Registrant Org": extract("Registrant Organization", r"Registrant Organization:\s+([^\n]+)"),
            "Registrant Country": extract("Registrant Country", r"Registrant Country:\s+([^\n]+)")
        }

        # Print clean summary
        print("\n" + "="*60)
        print("[ WHOIS Summary ]")
        print("="*60)
        for key, value in summary.items():
            print(f"{key:18}: {value}")
        print(f"\n[✓] Raw output also saved to: {output_path}")

    except Exception as e:
        print(f"[!] Error running WHOIS: {e}")
