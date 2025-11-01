#!/usr/bin/env python3
import sys, os, subprocess, re , requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import *

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def archive_org(domain):
    req = requests.get(f'https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&fl=timestamp,original&collapse=digest').text
    print(f"{colors.GRAY}Subdomain extraction from : archive.org{colors.RESET}")
    
    return req

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: bat_archive domain")
        sys.exit()

    program = Programs.objects(scopes=domain).first()

    if program:
        print(f"[{current_time()}] running archive.org module for '{domain}'")
        subs = archive_org(domain).split()
        # todo: save in file 

        # save in Bat-Tower datanbase
    
        filtered_data = [item for item in subs if not re.match(r'^\d+$', item)]
        for item in filtered_data:
            with open('res.text', 'a+') as data: 
                data.write(item + '\n')
        
        command =  subprocess.check_output('cat res.text | unfurl format %d | sort -u | uniq', shell=True, text=True)
        array = command.split()
        # unique_array = list(set(array))

        res_num = len(array) if array else 0
        print(f"{colors.GRAY}The number of subdomains that archive.org found for {domain}, results: {res_num}{colors.RESET}")
        
        for i in array:
            upsert_subdomain(program.program_name, i, 'archive')
        os.system('rm res.text')
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in Bat-Tower") 