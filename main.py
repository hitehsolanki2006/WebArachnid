# main.py

import argparse
from core.recon import whois_lookup, dns_enum, port_scan
from core.fingerprint import fingerprint
from core.enumeration import dir_enum
from core.scanning import vuln_scan



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
        'whois', 'dns','ports','fingerprint','direnum','vulnscan'  # <--- Added 'dns' module here
    ], help='Module to run')
    return parser.parse_args()

def main():
    banner()
    args = parse_args()

    if args.module == 'whois':
        whois_lookup.run(args.target)
    elif args.module == 'dns':
        dns_enum.run(args.target)
    elif args.module == 'ports':
        port_scan.run(args.target)
    elif args.module == 'fingerprint':
        fingerprint.run(args.target)
    elif args.module == 'direnum':
        dir_enum.run(args.target)
    elif args.module == 'vulnscan':
        vuln_scan.run(args.target)    
    else:
        print(f"[!] Module '{args.module}' not implemented yet.")

if __name__ == '__main__':
    main()
