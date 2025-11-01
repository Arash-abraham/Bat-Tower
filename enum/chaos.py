#!/usr/bin/env python3
import sys, os, subprocess, re ,requests , json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import *

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def chaos():
    print(f"{colors.GRAY}Subdomain extraction from : chaos{colors.RESET}")
    
if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: bat_chaos chaos_file.txt")
        sys.exit()
    
    program = Programs.objects(scopes=domain).first()
    
    if program:
        print(f"[{current_time()}] running chaos module")
        subs = subprocess.run(["zsh", "-c", f'cat ../Hilton/{domain}'], capture_output=True, text=True)
        result_lines = subs.stdout.splitlines()
        res_num = len(result_lines) if result_lines else 0
        print(f"{colors.GRAY}The number of subdomains that chaos found for {domain}, results: {res_num}{colors.RESET}")

        for i in result_lines:
            cleaned_line = re.sub(r'^\*\.?', '', i)
            if re.search(r'\.\s*' + re.escape(domain), cleaned_line, re.IGNORECASE):
                upsert_subdomain(program.program_name, cleaned_line, 'chaos')
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in Bat-Tower") 
