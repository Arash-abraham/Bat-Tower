#!/usr/bin/env python3
import sys, os, subprocess, re , tempfile , json
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

def creat_temp_file(data):
    with tempfile.NamedTemporaryFile(delete=False , mode='w') as temp_file:
        temp_file.write(data)
        return temp_file.name


def dnsx(subdomain_array,domain):

    with tempfile.NamedTemporaryFile(delete=False , mode='w') as temp_file:
        for sub in subdomain_array:
            temp_file.write(f'{sub}\n')
    
    subdomain_file = temp_file.name

    command = f"dnsx -l {subdomain_file} -wd {domain} -silent -rl 30 -t 10 -resp -json -r 8.8.4.4,129.250.35.251,208.67.222.222"
    print(f"{colors.GRAY}Executing commands: {command}{colors.RESET}")

    results = run_command_in_zsh(command)

    for result in results:
        obj = json.loads(result)
        upsert_lives({'domain': domain , 'subdomain': obj['host'] , 'ips': obj['a']})

    # return creat_temp_file(res)

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: bat_ns domain")
        sys.exit()

    obj_subs = Subdomains.objects(scope=domain)

    if obj_subs:
        print(f"[{current_time()}] running Dnsx module for '{domain}'")

        subs = [obj_sub.subdomain for obj_sub in obj_subs]

        dnsx(subs,domain)

        # for obj_sub in obj_subs:
        #     print(obj_sub.subdomain)
        
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in Bat-Tower") 