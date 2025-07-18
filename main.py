# main.py

import argparse
import os
from core.recon import whois_lookup

def banner():
    print(r"""
 __        __   _                            _     _      
 \ \      / /__| | ___ ___  _ __ ___   ___  | |__ (_) ___ 
  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | '_ \| |/ _ \
   \ V  V /  __/ | (_| (_) | | | | | |  __/ | | | | |  __/
    \_/\_/ \___|_|\___\___/|_| |_| |_|\___| |_| |_|_|\___|

      WebArachnid CLI — Target Analysis Toolkit
    """)

def parse_args():
    parser = argparse.ArgumentParser(description="WebArachnid CLI Scanner")
    parser.add_argument('--target', required=True, help='Target domain or IP')
    parser.add_argument('--module', required=True, choices=[
        'whois', 'dns', 'fingerprint', 'ports', 'enum', 'vuln', 'auth', 'exploit'
    ], help='Module to run')
    return parser.parse_args()

def main():
    banner()
    args = parse_args()

    if args.module == 'whois':
        whois_lookup.run(args.target)

    else:
        print(f"[!] Module '{args.module}' not implemented yet.")

if __name__ == '__main__':
    main()
