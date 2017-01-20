import urllib
from unidecode import unidecode
from lxml import etree



class ArXivParser():

    @staticmethod
    def get_all_authors(entry):
        if type(entry["author"]) == list:
            for e in entry["author"]:
                yield e["name"]["text"]
        else:
            yield entry["author"]["name"]["text"]

    def __init__(self):
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

        Output :

            - a dictionary: keys are tag name, or parameter names, or "text" for inner text,
              values can be: an other tag dictionary, or a list of those (if many tag with same name)
        """
        d = {}
        # getting attributes
        for k in tag.attrib:
            d[k] = tag.attrib[k]
            if type(d[k]) == unicode:
                d[k] = unidecode(d[k])
        # getting text
        d["text"] = tag.text
        if type(d["text"]) == unicode:
            d["text"] = unidecode(d["text"])

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
        if d.has_key("entry"):
            if not type(d["entry"]) == list:
                return [d["entry"]]
            return d["entry"]
        else:
            return []

    def entries_from_file(self, filename):
        parser = etree.XMLParser(encoding='utf-8')
        tree = etree.parse(filename, parser)
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

    baseURL = "http://export.arxiv.org/api/query"
    xmlns = "http://www.w3.org/2005/Atom"

    @staticmethod
    def get_new_entries(categories):
        """
        Return all entries of ``categories`` that have been published the previous day
        INPUT:

            - ``categories`` a list of string of arXiv Subject Classifications
        """
        from datetime import datetime
        from datetime import timedelta
        entries_per_page = 100
        parser = ArXivParser()
        parser.set_xmlns(ArXivRequest.xmlns)
        dateformat = "%Y-%m-%dT%H:%M:%SZ"
        request = RequestURL(ArXivRequest.baseURL)
        request.update_param("max_results", entries_per_page)
        request.update_param("sortBy","lastUpdatedDate")
        query = ArXivQuery("OR", [("cat", cat) for cat in categories])
        request.update_param("search_query", query.query_string())
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

    @staticmethod
    def get_all_entries(query):
        """
        Return all entries of ``query``
        INPUT:

            - ``query`` an ``ArXivQuery``
        """
        entries_per_page = 100
        parser = ArXivParser()
        parser.set_xmlns(ArXivRequest.xmlns)
        request = RequestURL(ArXivRequest.baseURL)
        request.update_param("max_results", entries_per_page)
        request.update_param("search_query", query.query_string())
        entries = []
        start = 0
        hasEntries = True
        while hasEntries:
            request.update_param("start",start)
            hasEntries = False
            new_entries = parser.entries_from_file(request.getURL())
            if len(new_entries) > 0:
                entries.extend(new_entries)
                start+= len(new_entries)
            if len(new_entries) == entries_per_page:
                hasEntries = True
        return entries

    @staticmethod
    def get_author_entries(author, categories = None):
        qAuth = ArXivQuery.get_author_query(author)
        if categories is not None:
            qCat = ArXivQuery("OR", [("cat", cat) for cat in categories])
            qAuth.add_query_element(qCat)
        return ArXivRequest.get_all_entries(qAuth)




class ArXivQuery():
    """
    A Class for the "search_query" parameter of an arXiv query
    """

    @staticmethod
    def get_author_query(fullname):
        fullname = fullname.replace("-","_")
        s = fullname.split(" ")
        return ArXivQuery("AND", query_elements = [("au", value) for value in s])

    def __init__(self, query_type, query_elements = None):
        """
        INPUT:

            - ``query_type`` a string, can be "AND" "OR" or "ANDNOT"
        """
        if query_elements is None:
            query_elements = []
        self._query_elements = query_elements
        self._query_type = query_type

    def query_type(self):
        return self._query_type



    def add_query_element(self, query_element):
        """
        Add a query_element to the query

        INPUT:

            - ``query_element`` can be either a tuple ``(key, value)``
              with ``key`` an arXiv field prefix
              or another ``ArXivQuery``
        """

        self._query_elements.append(query_element)


    def query_string(self):
        """
        Return the query string to serve for as a value for the arXiv
        search_query parameter
        """
        def element_string(element):
            if isinstance(element, ArXivQuery):
                return "%28" + element.query_string() + "%29"
            else:
                return element[0] + ":" + element[1]

        inter = "+" + self.query_type() + "+"
        return inter.join(element_string(e) for e in self._query_elements)
