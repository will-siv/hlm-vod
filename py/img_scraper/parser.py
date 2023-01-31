from xml.dom.minidom import parse, parseString
from lxml import html, etree
import sys

def main():
    file = sys.argv[1]

    with open(file, 'r', encoding='utf-8') as inp:
        htmldoc = html.fromstring(inp.read())

    with open("out.xml", 'wb') as out:
        out.write(etree.tostring(htmldoc))

    dom = parse("out.xml")

    for table in dom.getElementsByTagName("table"):
        if table.getAttribute("class") == "infobox bordered":
            for a in table.getElementsByTagName("a"):
                if a.getAttribute("class") == "image":
                    img = a.getElementsByTagName("img")[0]
                    srcset = img.getAttribute("srcset")
                    if srcset != '':
                        print(srcset.split(", ")[1][:-3])


if __name__ == "__main__":
    main()
