#!/usr/bin/env python3
import sys, os, subprocess, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import *

def run_command_in_zsh(command):
    try:
        result = subprocess.run(["zsh", "-c", command], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Error occurred:", result.stderr)
            return False

        return result.stdout.splitlines()
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"
    
def abuse(domain):

    command = f"/home/arash/Desktop/Bat-Tower/enum/abuse.sh {domain}"
    print(f"{colors.GRAY}Executing commands: abuse {domain}{colors.RESET}")
    res = run_command_in_zsh(command)

    res_num = len(res) if res else 0
    print(f"{colors.GRAY}The number of subdomains that abuseipdb found for {domain}, results: {res_num}{colors.RESET}")

    return res

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else None

    if domain is None:
        print(f"Usage: bat_abuseipdb domain")
        sys.exit()

    program = Programs.objects(scopes=domain).first()

    if program:
        print(f"[{current_time()}] running abuseipdb module for '{domain}'")
        subs = abuse(domain)

        if not isinstance(subs, (list, set)):
            print("Error: The function 'abuse' did not return a valid iterable.")
            sys.exit()

        for sub in subs:
            upsert_subdomain(program.program_name, sub, 'abuseipdb')
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in Bat-Tower")
