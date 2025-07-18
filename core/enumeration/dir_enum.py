# core/enumeration/dir_enum.py

import subprocess
import os

def run(target):
    print(f"[+] Starting Directory Bruteforce on {target}")
    try:
        os.makedirs("output", exist_ok=True)
        output_file = f"output/dir_enum_{target.replace('.', '_')}.txt"
        wordlist = "wordlists/web_dir.txt"  # or use full path to /usr/share/wordlists/dirb/common.txt

        url = f"http://{target}/"

        # Run ffuf
        print("[*] Running ffuf...")
        result = subprocess.run([
            'ffuf', '-w', wordlist,
            '-u', f"{url}FUZZ",
            '-mc', '200,301,302,403',
            '-t', '40',
            '-of', 'csv',
            '-o', output_file
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[!] ffuf error:\n{result.stderr}")
            return

        print("\n" + "="*60)
        print("[ Directory Enumeration Summary ]")
        print("="*60)

        # Read the CSV output
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                lines = f.readlines()[1:]  # Skip CSV header
                if not lines:
                    print("No results found.")
                else:
                    for line in lines:
                        parts = line.strip().split(',')
                        url = parts[1]
                        status = parts[2]
                        length = parts[3]
                        words = parts[4]
                        print(f"{status} | {url} | Len: {length} | Words: {words}")

        print(f"\n[✓] Output saved to: {output_file}")

    except Exception as e:
        print(f"[!] Directory enum failed: {e}")
