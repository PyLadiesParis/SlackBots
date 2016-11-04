import urllib
from lxml import etree
url = 'http://export.arxiv.org/api/query?search_query=math.CO&start=0&max_results=10&sortBy=lastUpdatedDate'
data = urllib.urlopen(url).read()


class ArXivParser():

    def __init__(self):
        pass
        self._xmlns = ""

    def set_xmlns(self, xmlns):
        self._xmlns = xmlns

    def get_xmlns(self):
        return self._xmlns

    def _clean_tag(self, tagname):
        """
        Remove xmlns from tag name
        """
        if self._xmlns != "":
            return tagname[len(self._xmlns)+2:] # +2 because of { }
        return tagname

    def _parse_tag(self, tag):
        """
        Return a dictoionary corresponding to the content of the etree tag
        Input :

            - tag, an etree tag
            - a dictionary: keys are tag name, or parameter names, or "text" for inner text,
              values can be: an other tag dictionary, or a list of those (if many tag with same name)
        """
        d = {}
        # getting attributes
        for k in tag.attrib:
            d[k] = tag.attrib[k]
        # getting text
        d["text"] = tag.text

        # getting children
        for e in tag:
            key = self._clean_tag(e.tag)
            v = self._parse_tag(e)
            if d.has_key(key):
                v2 = d[key]
                if type(v2) == list:
                    v2.append(v)
                else:
                    d[key] = [v2,v]
            else:
                d[key] = v

        return d

    def parse_etree(self, tree):
        root = tree.getroot()
        return self._parse_tag(root)

    def get_entries(self,tree):
        d = self.parse_etree(tree)
        return d["entry"]

    def entries_from_file(self, filename):
        tree = etree.parse(filename)
        return self.get_entries(tree)

class ArXivRequest():

    def __init__(self):
        self._categories = []
        self._parameters = {"max_results": 100,"sortBy":"lastUpdatedDate","start":0}
        self._baseurl = "http://export.arxiv.org/api/query"

    def add_category(self, category):
        self._categories.append(category)

    def getURL(self):
        return self._baseurl + "?search_query=" + "+".join(self._categories) + "&" + "&".join(k + "=" + str(self._parameters[k]) for k in self._parameters)

    def get_new_articles

#parser = ArXivParser()
#parser.set_xmlns("http://www.w3.org/2005/Atom")
#entries = parser.entries_from_file("textxml.xml")
#print entries

#for a in entries[0]["author"]:
    #print a["name"]["text"]


