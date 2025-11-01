#!/usr/bin/env python3
import sys, os, subprocess, requests, tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

from db import *

def send_discord_message(message):
    data = {
        "content": message
    }

    response = requests.post(config().get('WEBHOOK_URL'), json=data)

    if response.status_code == 204:
        pass
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

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

def nuclei(urls):

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        for url in urls:
            temp_file.write(f"{url}\n")
    
    urls_file = temp_file.name

    for url in urls:
        command = f"nuclei -l {urls_file} -config {config().get('WATCH_DIR')}/nuclei/public-config.yaml"

        print(f"{colors.GRAY}Executing commands: {command}{colors.RESET}")
    
        results = run_command_in_zsh(command)

        if results != '':
            send_discord_message(results)

    return True

if __name__ == "__main__":

    https_obj = Http.objects().all()

    if https_obj:
        print(f"[{current_time()}] running Nuclei module for all HTTP services")
        
        nuclei([http_obj.url for http_obj in https_obj])

    