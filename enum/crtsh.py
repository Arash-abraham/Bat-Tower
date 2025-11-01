#!/usr/bin/env python3
import sys, os, subprocess, re, psycopg2
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import *

class colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"

def crtsh(domain):
    def connect_with_retry(db_params, retries=5, delay=2):
        for i in range(retries):
            try:
                connection = psycopg2.connect(**db_params)
                return connection
            except psycopg2.OperationalError as e:
                print(f"Connection attempt {i + 1} failed: {e}")
                time.sleep(delay)
        raise Exception("Failed to connect to the database after several attempts.")

    print(f"{colors.GRAY}Executing commands: crtsh {domain}{colors.RESET}")

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
    connection = connect_with_retry(db_params)
    connection.autocommit = True

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, (domain,))
        results = cursor.fetchall()
        
        # Process results
        processed_results = set()
        for row in results:
            name_value = row[0].strip()
            if re.search(r'\.\s*' + re.escape(domain), name_value, re.IGNORECASE) and '*' not in name_value:
                processed_results.add(name_value.lower().replace(f'.{domain}', ''))
                
        # Output results
        res = [f"{sub}.{domain}" for sub in processed_results if sub != '*']
        res_num = len(res)
        print(f"{colors.GRAY}The number of subdomains that crtsh found for {domain}, results: {res_num}{colors.RESET}")

        return res
            
    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        # Clean up
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else False

    if domain is False:
        print(f"Usage: bat_crt domain")
        sys.exit()

    program = Programs.objects(scopes=domain).first()

    if program:
        print(f"[{current_time()}] running crtsh module for '{domain}'")
        subs = crtsh(domain)

        if subs is not None:
            for sub in subs:
                if re.search(r'\.\s*' + re.escape(domain), sub, re.IGNORECASE):
                    upsert_subdomain(program.program_name, sub, 'crtsh')
        else:
            pass
    else:
        print(f"[{current_time()}] scope for '{domain}' does not exist in Bat-Tower")
