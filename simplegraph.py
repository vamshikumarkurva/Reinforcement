import numpy as np

# reprsesenting graph using dictinary
graph_G={'A':['B','C'],
       'B':['C','D'],
       'C':['D'],
       'D':['C'],
       'E':['F'],
       'F':['E']}

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbor in graph[node]:
            edges.append((node,neighbor))
    return edges

def isolated_vertices(graph):
    isolated = []
    for node in graph:
        if not graph[node]:
            isolated.append(node)
    return isolated

print 'edges = ',generate_edges(graph_G)
print 'isolated vertices=',isolated_vertices(graph_G)

