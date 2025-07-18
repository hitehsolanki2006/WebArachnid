# core/recon/whois_lookup.py

import subprocess

def run(target):
    print(f"[+] Running WHOIS lookup for {target}")
    try:
        result = subprocess.run(['whois', target], capture_output=True, text=True)
        output_path = f"output/whois_{target}.txt"
        with open(output_path, 'w') as f:
            f.write(result.stdout)
        print(f"[✓] Output saved to {output_path}")
    except Exception as e:
        print(f"[!] Error running WHOIS: {e}")
