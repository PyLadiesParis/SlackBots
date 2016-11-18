import urllib
from lxml import etree


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

class RequestURL():

    def __init__(self, baseurl):
        self._parameters = {}
        self._baseurl = baseurl


    def update_param(self, param, value):
        self._parameters[param] = value

    def getURL(self):
        return self._baseurl + "?" + "&".join(k + "=" + str(self._parameters[k]) for k in self._parameters)

class ArXivRequest():

    def __init__(self):
        self._baseurl = "http://export.arxiv.org/api/query"
        self._categories = []
        self._extra_params = {} #todo


    def add_category(self, category):
        self._categories.append(category)

    def get_new_entries(self):
        from datetime import datetime
        from datetime import timedelta
        entries_per_page = 100
        parser = ArXivParser()
        parser.set_xmlns("http://www.w3.org/2005/Atom")
        dateformat = "%Y-%m-%dT%H:%M:%SZ"
        request = RequestURL(self._baseurl)
        request.update_param("max_results", entries_per_page)
        request.update_param("sortBy","lastUpdatedDate")
        request.update_param("search_query", "+".join(self._categories))
        yesterday = (datetime.today() - timedelta(days=1)).date()
        entries = []
        start = 0
        hasEntries = True
        while hasEntries:
            request.update_param("start",start)
            hasEntries = False
            for entry in parser.entries_from_file(request.getURL()):
                entrydate = datetime.strptime(entry["updated"]["text"], dateformat).date()
                if yesterday != entrydate:
                    break
                entries.append(entry)
            else:
                hasEntries = True
                start+= entries_per_page
        return entries




#parser = ArXivParser()
#parser.set_xmlns("http://www.w3.org/2005/Atom")
#entries = parser.entries_from_file("textxml.xml")
#print entries

#for a in entries[0]["author"]:
    #print a["name"]["text"]

