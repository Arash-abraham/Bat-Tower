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

def subfinder(domain):

    command = f"subfinder -d {domain} -all"
    print(f"{colors.GRAY}Executing commands: {command}{colors.RESET}")
    res = run_command_in_zsh(command)

    res_num = len(res) if res else 0
    print(f"{colors.GRAY}done for {domain}, results: {res_num}{colors.RESET}")

    return res

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: watch_subfinder domain")
        sys.exit()

    program = Programs.objects(scopes=domain).first()

    if program:
        print(f"[{current_time()}] running Subfinder module for '{domain}'")
        subs = subfinder(domain)
        # todo: save in file

        # save in watchtower datanbase
        for sub in subs:
            if re.search(r'\.\s*' + re.escape(domain), sub, re.IGNORECASE):
                upsert_subdomain(program.program_name, sub, 'subfinder')
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in watchtower")