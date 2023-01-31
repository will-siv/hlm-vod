#!/bin/bash

if [[ ! -e $1 ]]; then
    echo Invalid arg
    exit 1
fi

for line in $(cat $1); do
    echo Getting character $line
    curl -s https://www.ssbwiki.com/$line > out.html
    python3 parser.py out.html > links
    for link in $(cat links); do
        wget -q $link -P ../../imgs/ult_renders/
    done
    rm out.html out.xml
done
rm links

echo done
