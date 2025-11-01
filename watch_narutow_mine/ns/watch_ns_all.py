#!/usr/bin/env python3
import sys, os, subprocess, json, tempfile
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

def dnsx(subdomains_array, domain):

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        for sub in subdomains_array:
            temp_file.write(f"{sub}\n")
    
    subdomains_file = temp_file.name

    command = f"dnsx -l {subdomains_file} -silent -wd {domain} -rl 30 -t 10 -resp -json -r 8.8.4.4,129.250.35.251,208.67.222.222"
    # command = f"dnsx -l {subdomains_file} -silent -wd {domain} -resp -json -r 8.8.4.4,129.250.35.251,208.67.222.222"

    print(f"{colors.GRAY}Executing commands: {command}{colors.RESET}")
    
    results = run_command_in_zsh(command)

    for result in results:
        # todo: check if IP belongs to CDNs, add {'cdn': 'name_of_cdn'}
        obj = json.loads(result)
        upsert_lives({'subdomain': obj.get('host'), 'domain': domain, 'ips': obj.get('a'), 'cdn': ''})

    return True

if __name__ == "__main__":
    programs = Programs.objects().all()

    for program in programs:
        for scope in program.scopes:
            domain = scope
            obj_subs = Subdomains.objects(scope=domain)

            if obj_subs:
                print(f"[{current_time()}] running Dnsx module for '{domain}'")
                
                dnsx([obj_sub.subdomain for obj_sub in obj_subs], domain)

            else:
                print(f"[{current_time()}] domain '{domain}' does not exist in watchtower")