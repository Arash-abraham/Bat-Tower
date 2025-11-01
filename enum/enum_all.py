#!/usr/bin/env python3
import sys, os, subprocess, re , psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from colorama import *
from db import *
from config import Config
from subfinder import *
from crtsh import *
from assetfinder import *
from bat_abuseipdb import *

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def run_command_in_zsh(command):
    try:
        result = subprocess.run(["zsh", "-c", command], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Error occurred:", result.stderr)
            return False

        return result.stdout.splitlines()
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)


if __name__ == "__main__":
    programs = Programs.objects.all()
    
    
    for program in programs:
        print(f"[{current_time()}] Let's got for {program.program_name} program ... ")
        scopes = program.scopes

        if scopes:
            for scope in scopes:
                try:
                    print(f"[{current_time()}] enumerating subdomains for {scope} domain ... ")
                    sub_crtsh = crtsh(scope)
                    if sub_crtsh is not None:
                        for subs_crtsh in sub_crtsh:
                            if re.search(r'\.\s*' + re.escape(scope), subs_crtsh, re.IGNORECASE):
                                upsert_subdomain(program.program_name, subs_crtsh, 'crtsh') 
                    else:
                        pass
                except psycopg2.OperationalError:
                    print(Fore.RED+f'ERROR => {subs_crtsh}')
                subs_subfinder = subfinder(scope)
                for sub in subs_subfinder:
                    if re.search(r'\.\s*' + re.escape(scope), sub, re.IGNORECASE):
                        upsert_subdomain(program.program_name, sub, 'subfinder')
                subs_assetfinder = assetfinder(scope)
                for sub in subs_assetfinder:
                    if re.search(r'\.\s*' + re.escape(scope), sub, re.IGNORECASE):
                        upsert_subdomain(program.program_name, sub, 'assetfinder') 
                subs_abuse = abuse(scope)
                for sub in subs_abuse:
                    if re.search(r'\.\s*' + re.escape(scope), sub, re.IGNORECASE):
                        upsert_subdomain(program.program_name, sub, 'abuseipdb') 
                
        
        else:
            print(f"[{current_time()}] scope for '{domain}' does not exist in Bat-Tower") 
        