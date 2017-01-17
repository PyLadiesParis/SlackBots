from arxivrequest import ArXivRequest
from arxivrequest import ArXivParser

class CollaboratorGraph():

    def __init__(self):
        self._collaborations = {}
        self._neighbors = {}

    def __iter__(self):
        for c in self._neighbors:
            yield c

    def __contains__(self, author):
        return author in self._neighbors

    def __len__(self):
        return len(self._neighbors)

    def __repr__(self):
        return "Collaborator graph with " + str(len(self)) + " collaborators and " + str(len(self._collaborations)) + " collaborations"


    def neighbors(self, auth):
        for n in self._neighbors[auth]:
            yield n

    def add_collaboration(self, auth1, auth2, n = 1):
        def add_edge(auth1, auth2):
            if auth1 in self:
                self._neighbors[auth1].add(auth2)
            else:
                self._neighbors[auth1] = {auth2}
        k = (auth1, auth2)
        if not (auth2, auth1) in self._collaborations:
            self._collaborations[k] = self._collaborations.get(k, 0) + n
            add_edge(auth1, auth2)
            add_edge(auth2, auth1)

    def collaborations(self, auth1, auth2):
        if self._collaborations.has_key((auth1,auth2)):
            return self._collaborations[(auth1,auth2)]
        return self._collaborations.get((auth2,auth1), 0)

    def iter_collaborations(self):
        for k in self._collaborations:
            yield k[0], k[1], self._collaborations[k]

    def fusion_graph(self,g2):
        for auth1, auth2, v2 in g2.iter_collaborations():
            v1 = self.collaborations(auth1,auth2)
            if v1 < v2:
                self.add_collaboration(auth1, auth2, v2 - v1)


class CollaboratorFinder():

    @staticmethod
    def update_graph(graph, author, categories = None, ignore_entries = None):
        """
        Look for ``author`` direct collaborators on arXiv and update the graph
        accordingly

        INPUT:

            - ``graph`` a ``CollaboratorGraph``
            - ``author`` the author to look for

        OUTPUT:

            - a list of new collaborators (who where not already present in the graph)
        """
        if ignore_entries is None:
            ignore_entries = []
        E = ArXivRequest.get_author_entries(author, categories)
        new_authors = []
        for entry in E:
            eid = entry["id"]["text"][21:-2]
            if not eid in ignore_entries:
                for collaborator in ArXivParser.get_all_authors(entry):
                    if author != collaborator:
                        if not collaborator in graph:
                            new_authors.append(collaborator)
                        graph.add_collaboration(author, collaborator)
        return new_authors


    @staticmethod
    def create_graph(entry_points, distance, categories = None, graph = None, ignore_entries = None):
        if distance == 0:
            return graph
        if graph is None:
            graph = CollaboratorGraph()
        next_level = []
        for author in entry_points:
            next_level.extend(CollaboratorFinder.update_graph(graph, author, categories, ignore_entries = ignore_entries))
        return CollaboratorFinder.create_graph(next_level, distance -1, categories, graph, ignore_entries = ignore_entries)


#def get_weighted_collaborators(g, origin, distancemax):
    #_weights = {c:0 for c in g}
    #def visit(node1, node2, distance, weight):
        #if node2 != origin:
            #weight+= float(g.collaborations(node1,node2))/(distance**4)
            #_weights[node2]+= weight
        #if distance != distancemax:
            #for n in g.neighbors(node2):
                #if n != node1 and n != origin:
                    #visit(node2, n, distance+1, weight)
    #visit(origin, origin, 0, 1)
    #return _weights

def get_weighted_collaborators(g, origin, distancemax):
    _weights = {c:0 for c in g}
    def visit(node1, node2, distance, p):
        if node2 != origin:
            _weights[node2]+=p
        if distance != distancemax:
            N = list(n for n in g.neighbors(node2) if n != node1 and n != origin)
            s = sum(g.collaborations(node2,n) for n in N)
            for n in N:
                visit(node2, n, distance+1, p*float(g.collaborations(node2,n))/s)
    visit(origin, origin, 0, 1.)
    return _weights
