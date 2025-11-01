# Bat-Tower 🦇

Welcome to Bat-Tower - Your reconnaissance and monitoring toolkit!

## ⚡ Quick Setup

### Installation
1. Download the `Bat-Tower` files
2. Place the files in your `$HOME` directory
3. Configure Bat-Tower
   - Open `config.py`
   - Edit the `BAT_DIR` variable to the path where the Bat-Tower folder is located
   - To push results to Discord, add the Discord webhook in `config.py`

4. Install Requirements:
```   pip install -r requirements.txt```

If there is a problem during installation, add the following items to the requirements.txt file:
flask`
`psycopg2`
`psycopg2-binary`
`mongoengine`

`5. Example Command:`
`bat_ns google.com`
`cat /tmp/tmptzj0axl7`

`Example output:`
`hash-att.google.com`
`r.google.com`
`attacker.google.com`
`www.google.com`
`.`
`.`
`.`

### 🚀 Aliases Configuration

`Add these aliases to your ~/.zshrc:`

`alias bat_sync_programs=`python $HOME/Bat-Tower/programs/sync_programs.py``
`alias bat_sync_subfinder=`python $HOME/Bat-Tower/enum/subfinder.py``
`alias bat_sync_crtsh=`python $HOME/Bat-Tower/enum/crtsh.py``
`alias bat_enum_all=`python $HOME/Bat-Tower/enum/enum_all.py``
