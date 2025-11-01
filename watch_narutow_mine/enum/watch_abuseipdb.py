#!/usr/bin/env python3
import sys, os, subprocess, re, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import *

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def abuseipdb(domain):
    url = f"https://www.abuseipdb.com/whois/{domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }
    cookies = {
        "abuseipdb_session": "YOUR-SESSION",  # Replace YOUR-SESSION with your actual session ID
    }

    print(f"{colors.GRAY}Requesting URL: {url}{colors.RESET}")
    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code != 200:
        print(f"Error occurred: {response.status_code} - {response.reason}")
        return []

    # Extracting the data using regex
    results = re.findall(r'<li>(\w.*)</li>', response.text)
    results = [f"{result.strip()}.{domain}" for result in results]

    print(f"{colors.GRAY}done for {domain}, results: {len(results)}{colors.RESET}")

    return results

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: watch_abuseipdb domain")
        sys.exit()

    program = Programs.objects(scopes=domain).first()

    if program:
        print(f"[{current_time()}] running abuseipdb module for '{domain}'")
        subs = abuseipdb(domain)
        # todo: save in file

        # save in watch database
        for sub in subs:
            if re.search(r'\.\s*' + re.escape(domain), sub, re.IGNORECASE):
                upsert_subdomain(program.program_name, sub, 'abuseipdb')
                # print(sub)

    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in watch-tower")