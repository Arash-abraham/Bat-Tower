#!/usr/bin/env python3

import os , json ,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' )))


from db import upsert_program
from config import Config

def scan_directory_for_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory,filename)
            print(f'Processing file : {file_path}')

            with open(file_path , 'r') as file:
                try:
                    data = json.load(file)
                    # print(1)
                    upsert_program(data.get('program_name'), data.get('scope') , data.get('ooscope') , {} )
                except json.JSONDecodeError as e:
                    print(f'{file_path} : {e}')


if __name__ == "__main__":
    # print(Config().get('BAT_DIR'))
    directory_to_scan = Config().get('BAT_DIR')+'/programs/'
    scan_directory_for_json_files(directory_to_scan)