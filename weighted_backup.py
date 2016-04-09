import numpy as np
import operator

class Graph(object):
 
    # Initializes the graph object
    def __init__(self, graphdict={}):
        self._graph_dict = graphdict
    
    # returns the vertices of graph object
    def vertices(self):
        return list(self._graph_dict.keys())

    # returns the edges of graph object
    def edges(self):
        return self._generate_edges()

    # add a vertex to the graph
    def add_vertex(self, vertex):
        if vertex in self._graph_dict:
            print "%s is already in graph" %vertex
        else:
            self._graph_dict[vertex] = {}

    # add a weighted edge to the graph
    def add_edge(self, edge, _weight=1.0):
        (vertex1,vertex2) = edge
        weight = _weight

        # since undirected graph, add the connection fron v1--->v2 and v2---->v1 with the same weight 
        if vertex1 in self._graph_dict:
            self._graph_dict[vertex1][vertex2] = weight
        else:
            self._graph_dict[vertex1] = {vertex2:weight}
        if vertex2 in self._graph_dict:
            self._graph_dict[vertex2][vertex1] = weight
        else:
            self._graph_dict[vertex2] = {vertex1:weight}

    #generate the edges from the connections given
    def _generate_edges(self):
        edges=[]
        for node in self._graph_dict:
            for connection in self._graph_dict[node]:
                if (node, connection, self._graph_dict[node][connection]) and (connection, node, self._graph_dict[node][connection]) not in edges: 
                    edges.append( (node, connection, self._graph_dict[node][connection]) )
        return edges
  
    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self._generate_edges():
            res += str(edge) + " "
        return res

    # to find isolated vertices in the graph
    def isolated_vertices(self):
        isolated = []
        for node in self._graph_dict:
            if not self._graph_dict[node]:
                isolated += node
        return isolated        

    def return_label(self,present = None,previous = None,original = None,label=dict(),visited=list()):
        if present is None:
            vertices = self.vertices()
            present = vertices[0]
            for vertex in vertices:
                label[vertex] = 0
            original = present
        if self._graph_dict[present]:
            for next in self._graph_dict[present]:
                if previous!=next:
                    if next==original:
                        label[next] += 1
                    if next not in visited:
                        label[next] += 1
                        visited.append(next)
                        if next!=original:
                            label=self.return_label(next, present,original,label,visited)
                            visited.remove(next)
        return label
        

    def is_acyclic(self):
        vertices = self.vertices()
        present = vertices[0]
        label = self.return_label()
        #print "No of paths from ", present, " to other vertices: " 
        label1 = dict()
        for key in label:
            if key in vertices:
                label1[key] = label[key]
        print label1
        for key in label1:
            if label1[key] > 1:
                return False
        return True

    # To check connectedness of the graph
    def is_connected(self):
        vertices = self.vertices()
        present = vertices[0]
        label = self.return_label()
        #print "No of paths from ", present, " to other vertices: " 
        label1 = dict()
        for key in label:
            if key in vertices:
                label1[key] = label[key]
        print label1
        label1[present] += 1
        for key in label1:
            if label1[key]==0:
                return False
        return True
    
    def find_MST_kruskal(self):
        if not self.is_connected():
            return False
        edges = self.edges()
        vertices = self.vertices()
        edges.sort(key=operator.itemgetter(2))
        E = len(edges)     
        MST = Graph({})
        MST.add_edge((edges[0][0],edges[0][1]),edges[0][2])
        MST_dup = Graph({})
        count = 1
        N = len(vertices)
        i = 1
        
        while count!=N-1: 
            MST_dup = MST
            MST_dup.add_edge((edges[i][0],edges[i][1]),edges[i][2])
            if MST_dup.is_acyclic():
                MST.add_edge((edges[i][0],edges[i][1]),edges[i][2])
                count += 1
            i += 1 
            if i > E-1:
                break
        return MST


    def find_MST_prim(self):
        if not self.is_connected():
            return False
        vertices = self.vertices()  
        MST1 = Graph({})
        v1 = vertices[0]
        x = self._graph_dict[v1]
        y = sorted(x.items(),key=operator.itemgetter(1))
        v2 = y[0][0]
        MST1.add_edge((v1,v2),y[0][1])
        MST1_dup=Graph({})
        count = 1
        min_link=dict()
        N = len(vertices)
        while count!=N-1:
            MST1_dup = MST1
            for vertex in MST1.vertices():
                x = self._graph_dict[vertex]
                y = sorted(x.items(),key=operator.itemgetter(1))
                for v in MST1.vertices():
                    if v in x: 
                        if (v,x[v]) in y:
                            y.remove((v,x[v]))
                if y:
                    min_link[vertex] = {y[0][0]:y[0][1]}
            min_list = [(v1,v2,w) for v1 in min_link for v2,w in min_link[v1].items()]
            min_list.sort(key=operator.itemgetter(2))
            for i in range(len(min_list)):
                MST1_dup.add_edge((min_list[i][0],min_list[i][1]),min_list[i][2])
                if MST1_dup.is_acyclic():
                    MST1.add_edge((min_list[i][0],min_list[i][1]),min_list[i][2])
                    count += 1
                    break
        return MST1

    def find_shortest_path(self,start_v,end_v):
        vertices = self.vertices()
        if start_v not in vertices:
            return False
        if end_v not in vertices:
            return False
        dist = dict()
        previous=dict()
        B=[]
        for v in vertices:
            dist[v] = float("inf")
        dist[start_v]=0
        u = None
        
        while u!= end_v:
            min_v = None
            min_dist = None
            for v in vertices:
                if v not in B:
                    if min_v is None:
                        min_v = v
                    if min_dist is None:
                        min_dist = dist[v]
                    if dist[v] < min_dist:
                        min_v = v
                        min_dist = dist[v]
            u = min_v
            B.append(u)
            if u==end_v:
                break
            for v in self._graph_dict[u]:
                if v not in B:
                    if dist[u]+graph._graph_dict[u][v] < dist[v]:
                        dist[v] = dist[u]+graph._graph_dict[u][v]
                        previous[v] = u
        shortest_path=[]
        v = end_v
        while v!=start_v:
            shortest_path.append(v)
            v = previous[v]
        shortest_path.append(v)
        shortest_path.reverse()
        shortest_path.append(dist[end_v])
        return shortest_path
                
def menu():
    print "1. Add vertex "
    print "2. add an edge "
    print "3. Display the vertices "
    print "4. Display the edges "
    print "5. Display the isolated vertices "
    print "6. Is connected?: "
    print "7. Is acyclic?: "
    print "8. Find MST(Minimal Spanning Tree, Kruskal's Algo): "
    print "9. Find MST(Minimal Spanning Tree, Prim's Algo): "
    print "10. Find shortest path (Dijkstra's algo):  "
    print "11. Exit "

def verify(x):
    try:
        ch = int(x)
    except:
        print "Incorrect input."
        return -1
    return ch

# main program
if __name__ == "__main__":

    g = { "a" : {"b":10,"c":2,"d":7},
          "b" : {"c":6,"a":10},
          "c" : {"b":6, "a":2, "d":5},
          "d" : {"a":7, "c":5}
        }

    g1 = { "a" : {"b":1, "g":15},
           "b" : {"a":1, "c":4, "f":25},
           "c" : {"b":4, "d":7,  "f":2},
           "d" : {"c":7, "e":30},
           "e" : {"d":30, "f":10},
           "f" : {"b":25, "g":11, "h":8, "c":2, "e":10},
           "g" : {"a":15, "f":11, "h":10},
           "h" : {"g":10, "f":8}
         }

    
    #graph = Graph({})
    graph = Graph()
    # Initialization of the graph
    while(True):
        menu()
        x = raw_input("enter your choice: ")
        ch = verify(x)
        if ch==1:
            v = raw_input("Enter vertex: ")
            graph.add_vertex(v)
            print "Vertices of graph: "
            print graph.vertices() 
        elif ch==2:
            edge = tuple(raw_input("Enter edge(Use comma as separator,default weight=1): ").split(','))
            if len(edge)==3:
                (v1,v2,weight) = edge
                try:
                    weight = float(weight)
                except:
                    print "Weight must be a number"
                    break
                graph.add_edge((v1,v2),weight)
            else:
                (v1,v2) = edge
                graph.add_edge((v1,v2))
            print "Edges of graph: "
            print graph.edges()
        elif ch==3:
            print "Vertices of graph: "
            print graph.vertices()
        elif ch==4:
            print "Edges of graph: "
            print graph.edges()
        elif ch==5:
            print "Isolated vertices: "
            print graph.isolated_vertices()
        elif ch==6:
            if graph.is_connected():
                print "Graph is Connected"
            else:
                print "Graph is Disconnected"
        elif ch==7:
            if graph.is_acyclic():
                print "Graph is Acyclic"
            else:
                print "Graph is Cyclic"
        elif ch==8:
            MST = graph.find_MST_kruskal()
            if MST:
                print "MST: ",MST.edges()
            else:
                print "Graph is not connected. Can't find MST"
        elif ch==9:
            MST1 = graph.find_MST_prim()
            if MST:
                print "MST: ",MST.edges()
            else:
                print "Graph is not connected. Can't find MST"
        elif ch==10:
            (v1,v2) = tuple(raw_input("Enter start and End vertices(Use comma as separator): ").split(','))
            k = 0
            if v1 not in graph.vertices():
                print v1, "is not in graph"
                k = 1
            if v2 not in graph.vertices():
                print v2, "is not in graph"
                k = 1
            if k!=1:
                print graph.find_shortest_path(v1,v2)
        elif ch==11:
            break
    # Done
    
   



