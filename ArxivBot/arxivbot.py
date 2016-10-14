import urllib
from lxml import etree
url = 'http://export.arxiv.org/api/query?search_query=math.CO&start=0&max_results=10&sortBy=lastUpdatedDate'
data = urllib.urlopen(url).read()
tree = etree.parse("textxml.xml")
print tree
root = tree.getroot()
print root.tag
print root
print list(root)


def parseEntry(entry):
    for element in entry:
        print element
