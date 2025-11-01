# Bat-Tower
Welcome to my Bat Tower :)

## zshrc configurations

add following lines to your `~/.zshrc` file:

```bash
alias bat_sync_programs="The path where the file is located. /Bat-Tower/programs/sync_programs.py"
alias bat_sync_subfinder="The path where the file is located. /Bat-Tower/enum/subfinder.py"
alias bat_sync_crtsh="The path where the file is located. /Bat-Tower/enum/crtsh.py"
alias bat_enum_all="The path where the file is located. /Bat-Tower/enum/enum_all.py"
```


# Bat-Tower Installation and Setup Guide

1. **Download the Bat-tower files**
2. **Place the files in your `$HOME` directory**
3. **Configure Bat-tower**
    - Open `config.py`
    - Edit the `BAT_DIR` variable to the path where the Bat-tower folder is located.
    - To push results to Discord, add the Discord webhook in `config.py`.

4. **Install Requirements:**
    - If there is a problem during installation, add the following items to the `requirements.txt` file:
      ```
      flask
      psycopg2
      psycopg2-binary
      mongoengine
      ```
      
5. **Example Command:**
    ```bash
    bat_ns google.com
    cat /tmp/tmptzj0axl7
    ```
    - Example output:
      ```
      hash-att.google.com
      r.google.com
      attacker.google.com
      www.google.com
      .
      .
      .
      ```
