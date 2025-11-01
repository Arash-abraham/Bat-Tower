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

        return result.stdout
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def create_temp_file(data):
    # Create a temporary file and open it in write mode
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        # Write data to the temporary file
        temp_file.write(data)
        # Return the name of the temporary file
        return temp_file.name

def httpx(subdomains_array, domain):

    for subdomain in subdomains_array:
        command = f"echo {subdomain} | httpx -silent -json -favicon -fhr -title -tech-detect -irh -include-chain -timeout 3 -retries 1 -threads 5 -rate-limit 4 -ports 443 -extract-fqdn -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0' -H 'Referer: https://{subdomain}'"

        print(f"{colors.GRAY}Executing commands: {command}{colors.RESET}")
    
        results = run_command_in_zsh(command)

        if results != '':
            json_obj = json.loads(results)
            upsert_http({
                "subdomain": subdomain,
                "scope": domain,
                "ips": json_obj.get('a', ''),
                "tech": json_obj.get('tech', []),
                "title": json_obj.get('title', ''),
                "status_code": json_obj.get('status_code', ''),
                "headers": json_obj.get('header', {}),
                "url": json_obj.get('url', ''),
                "final_url": json_obj.get('final_url', ''),
                "favicon": json_obj.get('favicon', '')
            })

    return True

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: bat_httpx domain")
        sys.exit()

    obj_lives = LiveSubdomains.objects(scope=domain)

    if obj_lives:
        print(f"[{current_time()}] running HTTPx module for '{domain}'")
        
        httpx([obj_live.subdomain for obj_live in obj_lives], domain)

    