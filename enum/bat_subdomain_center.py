#!/usr/bin/env python3
import sys, os, subprocess, re ,requests , json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import *

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def api_subdomain_center(domain):
    req = requests.get(f'https://api.subdomain.center/?domain={domain}').text
    print(f"{colors.GRAY}Subdomain extraction from : api.subdomain.center{colors.RESET}")
    
    return req

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: bat_subdomain_center domain")
        sys.exit()

    program = Programs.objects(scopes=domain).first()

    if program:
        print(f"[{current_time()}] running api.subdomain.center module for '{domain}'")
        subs = json.loads(api_subdomain_center(domain))
        
        res_num = len(subs) if subs else 0
        print(f"{colors.GRAY}The number of subdomains that api.subdomain.center found for {domain}, results: {res_num}{colors.RESET}")
        
        for i in subs:
            upsert_subdomain(program.program_name, i, 'api.subdomain.center')

    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in Bat-Tower") 