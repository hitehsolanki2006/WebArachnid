# core/fingerprint/fingerprint.py

import subprocess
import os
import re

def parse_whatweb(raw_output):
    lines = raw_output.strip().splitlines()
    parsed = []

    for line in lines:
        if not line.startswith("http"):
            continue

        url_part, *rest = line.split(" ", 1)
        info = rest[0] if rest else ""

        # Extract fields
        data = {
            "URL": url_part,
            "Status": re.search(r"\[(\d+ .+?)\]", line),
            "Country": re.search(r"Country\[(.*?)\]", line),
            "IP": re.search(r"IP\[(.*?)\]", line),
            "Title": re.search(r"Title\[(.*?)\]", line),
            "Cookies": re.search(r"Cookies\[(.*?)\]", line),
            "HttpOnly": re.search(r"HttpOnly\[(.*?)\]", line),
            "Redirect": re.search(r"RedirectLocation\[(.*?)\]", line),
            "Server": re.search(r"HTTPServer\[(.*?)\]", line),
            "XFO": re.search(r"X-Frame-Options\[(.*?)\]", line),
            "XSS": re.search(r"X-XSS-Protection\[(.*?)\]", line),
            "Tech": re.findall(r",\s?(HTML5|Script|JQuery|PHP|ASP.NET|Drupal|WordPress|JavaScript)", line)
        }

        # Cleanup extracted values
        for k, v in data.items():
            if isinstance(v, re.Match):
                data[k] = v.group(1)
            elif isinstance(v, list):
                data[k] = ', '.join(set(v))
            elif not v:
                data[k] = 'N/A'

        parsed.append(data)
    return parsed

def run(target):
    print(f"[+] Running Web Fingerprinting on {target}")
    try:
        os.makedirs("output", exist_ok=True)
        output_file = f"output/fingerprint_{target.replace('.', '_')}.txt"
        url = f"http://{target}"

        print("[*] Launching WhatWeb scan...")
        result = subprocess.run(['whatweb', '--color=never', '--log-verbose=-', url],
                                capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout:
            print(f"[!] WhatWeb error:\n{result.stderr}")
            return

        raw_output = result.stdout.strip()

        # Save raw output
        with open(output_file, 'w') as f:
            f.write(raw_output)

        # Parse and print
        entries = parse_whatweb(raw_output)

        print("\n" + "="*60)
        print("[ WhatWeb Summary ]")
        print("="*60)

        for e in entries:
            print(f"\nTarget URL         : {e['URL']}")
            if e['Redirect'] != 'N/A':
                print(f"Final URL          : {e['Redirect']}")
            print(f"Status             : {e['Status']}")
            print(f"IP Address         : {e['IP']}")
            print(f"Country            : {e['Country']}")
            print(f"Server             : {e['Server']}")
            print(f"Title              : {e['Title']}")
            print(f"Cookies            : {e['Cookies']}")
            print(f"HttpOnly Cookies   : {e['HttpOnly']}")
            print(f"Security Headers   : XFO={e['XFO']}, XSS={e['XSS']}")
            print(f"Other Tech         : {e['Tech']}")

        print(f"\n[✓] Fingerprint report saved to: {output_file}")

    except Exception as e:
        print(f"[!] Fingerprint scan failed: {e}")
