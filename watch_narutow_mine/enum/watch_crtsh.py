#!/usr/bin/env python3
import sys, os, subprocess, psycopg2, re
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

def crtsh(domain):
    # Database connection parameters
    db_params = {
        'dbname': 'certwatch',
        'user': 'guest',
        'password': '',  # Add password if required
        'host': 'crt.sh',
        'port': 5432
    }
    
    # SQL query
    query = f"""
    SELECT
        ci.NAME_VALUE
    FROM
        certificate_and_identities ci
    WHERE
        plainto_tsquery('certwatch', %s) @@ identities(ci.CERTIFICATE)
    """

    # Establish connection and execute query
    connection = psycopg2.connect(**db_params)
    connection.autocommit = True

    try:
        cursor = connection.cursor()
        cursor.execute(query, (domain,))
        results = cursor.fetchall()
        
        # Process results
        processed_results = set()
        for row in results:
            name_value = row[0].strip()
            # todo: filter subdomains
            if re.search(r'\.\s*' + re.escape(domain), name_value, re.IGNORECASE) and '*' not in name_value:
                processed_results.add(name_value.lower().replace(f'.{domain}', ''))
                
        # Output results
        res = []
        for sub in list(processed_results):
            if sub != '*':
                res.append(f"{sub}.{domain}")

        return res
            
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        
    finally:
        # Clean up
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: watch_subfinder domain")
        sys.exit()

    program = Programs.objects(scopes=domain).first()

    if program:
        print(f"[{current_time()}] running Crtsh module for '{domain}'")
        subs = crtsh(domain)
        # todo: save in file
        # save in watchtower datanbase
        for sub in subs:
            upsert_subdomain(program.program_name, sub, 'crtsh')
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in watchtower")