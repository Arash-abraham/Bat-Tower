#!/bin/bash

if [ "$#" -ne 1 ]; then
    # echo "Usage: ./abuseipdb.sh <IP_ADDRESS>"
    exit 1
fi

curl -s "https://www.abuseipdb.com/whois/$1" \
-H "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" \
-b "abuseipdb_session=YOUR-SESSION" | \
grep --color=auto -E '<li>\w.*</li>' | \
sed -E 's/<\/?li>//g' | \
sed "s|$|.$1|"
