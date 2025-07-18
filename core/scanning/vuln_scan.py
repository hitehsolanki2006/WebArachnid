# core/scanning/vuln_scan.py

import subprocess
import os

def run(target):
    print(f"[+] Starting Vulnerability Scanning on {target}")
    try:
        os.makedirs("output", exist_ok=True)
        output_file = f"output/vulnscan_{target.replace('.', '_')}.txt"
        url = f"http://{target}"  # You can add https logic later

        with open(output_file, 'w') as f:
            def run_tool(name, cmd):
                print(f"[*] Running {name}...")
                f.write(f"\n=== {name} ===\n")
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    output = result.stdout.strip() if result.stdout else "[No output]"
                    print(f"[✓] {name} completed.")
                    f.write(output + "\n")
                except Exception as e:
                    err = f"[!] {name} failed: {e}"
                    print(err)
                    f.write(err + "\n")

            run_tool("Nikto", ['nikto', '-h', url, '-nointeractive'])
            run_tool("Nuclei", ['nuclei', '-u', url, '-silent'])

        print("\n[✓] Vulnerability scan report saved to:")
        print(f"    {output_file}")

    except Exception as e:
        print(f"[!] Vulnerability scan failed: {e}")
