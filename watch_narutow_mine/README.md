# watchtower
welcome to my watchtower :)

## setup the watch
1. inside the watchtower folder run `docker compose up -d`
2. modify `config.py` and put your own directory
3. configure zsh alias variables

## zshrc configurations
add following lines to your `~/.zshrc` file:
```bash
alias watch_sync_programs="/opt/watch_narutow/programs/watch_sync_programs.py"
alias watch_subfinder="/opt/watch_narutow/enum/watch_subfinder.py"
alias watch_crtsh="/opt/watch_narutow/enum/watch_crtsh.py"
alias watch_abuseipdb="/opt/watch_narutow/enum/watch_abuseipdb.py"
alias watch_enum_all="/opt/watch_narutow/enum/watch_enum_all.py"
alias watch_ns="/opt/watch_narutow/ns/watch_ns.py"
alias watch_ns_all="/opt/watch_narutow/ns/watch_ns_all.py"
alias watch_http="/opt/watch_narutow/http/watch_http.py"
alias watch_http_all="/opt/watch_narutow/http/watch_http_all.py"
alias watch_nuclei_all="/opt/watch_narutow/nuclei/watch_nuclei_all.py"
```

# Watchtower Installation and Setup Guide

1. **Download the Watchtower files**
2. **Place the files in your `$HOME` directory**
3. **Configure Watchtower**
    - Open `config.py`
    - Edit the `WATCH_DIR` variable to the path where the Watchtower folder is located.
    - To push results to Discord, add the Discord webhook in `config.py`.

4. **Install Requirements:**
    - If there is a problem during installation, add the following items to the `requirements.txt` file:
      ```
      flask
      psycopg2
      psycopg2-binary
      mongoengine
      ```

5. **Install Dependencies:**
    ```bash
    cd watch_narutow/
    pip3 install -r requirements.txt
    sudo apt-get install libpq-dev
    ```

6. **Set up Aliases in `.zshrc`:**
    ```bash
    alias watch_sync_programs="/home/w3ndgo/watch_narutow/programs/watch_sync_programs.py"
    alias watch_subfinder="/home/w3ndgo/watch_narutow/enum/watch_subfinder.py"
    alias watch_crtsh="/home/w3ndgo/watch_narutow/enum/watch_crtsh.py"
    alias watch_enum_all="/home/w3ndgo/watch_narutow/enum/watch_enum_all.py"
    alias watch_ns="/home/w3ndgo/watch_narutow/ns/watch_ns.py"
    alias watch_ns_all="/home/w3ndgo/watch_narutow/ns/watch_ns_all.py"
    ```

7. **Source the `.zshrc` file:**
    ```bash
    source .zshrc
    ```

8. **Make Scripts Executable:**
    ```bash
    chmod +x /home/w3ndgo/watch_narutow/programs/watch_sync_programs.py
    chmod +x /home/w3ndgo/watch_narutow/enum/watch_subfinder.py
    chmod +x /home/w3ndgo/watch_narutow/enum/watch_crtsh.py
    chmod +x /home/w3ndgo/watch_narutow/enum/watch_enum_all.py
    chmod +x /home/w3ndgo/watch_narutow/ns/watch_ns.py
    chmod +x /home/w3ndgo/watch_narutow/ns/watch_ns_all.py
    ```

9. **Edit Your Targets:**
    - Edit target files in the `programs` folder as per the provided examples.

10. **Run MongoDB with Docker:**
    ```bash
    cd database/
    docker compose up -d
    ```

11. **Run `app.py`:**
    ```bash
    flask --app app.py --debug run
    ```

12. **Finalize Installation:**
    - Now, Watchtower is installed and ready to use.
    - Add `watch.sh` to your cron jobs.

13. **Additional Tools:**
    - Install MongoDB Compass on your PC and connect to the database using the following URI:
      ```
      mongodb://127.0.0.1:27017
      ```
      *Note: If you're running it on a VPS, you'll need to set up port forwarding.*

14. **Using the API:**
    - You can use the API with `curl`. For example:
      ```bash
      curl -s http://127.0.0.1:5000/api/subdomains/icollab.info
      ```

15. **Commands for Sync & Enumeration of Subdomains:**
    - **Tip:** To use `watch_crtsh`, `watch_subfinder`, and other modules, you must define a scope in the `programs` folder.
    - Available commands:
      ```bash
      watch_sync_programs
      watch_enum_all
      watch_ns_all
      ```

16. **Example Command:**
    ```bash
    watch_ns icollab.info
    cat /tmp/tmptzj0axl7
    ```
    - Example output:
      ```
      hash-att.icollab.info
      r.icollab.info
      attacker.icollab.info
      www.icollab.info
      .
      .
      .
      ```
