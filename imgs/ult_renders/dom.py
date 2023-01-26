from xml.dom.minidom import parse, parseString
from lxml import html, etree

file = "Fighter_number"


with open(file, 'r', encoding='utf-8') as inp:
    htmldoc = html.fromstring(inp.read())

with open("out.xml", 'wb') as out:
    out.write(etree.tostring(htmldoc))


dom = parse("out.xml")

html = dom.firstChild

for element in html:
    if 


# 1: element node
# 3: text node

# i think i'm just gonna search the doc recursively and then pick out all of the tags from the table with numbers and all that
# if i had sat and manually downloaded all of the pictures i think i would be done by now but that's not COOL ENOUGH
