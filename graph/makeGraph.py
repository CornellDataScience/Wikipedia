import networkx as nx
import pandas as pd
import similarity as sm

#makes a graph based on the original format of the data, with depth 1
#mainly to provide data for random walks
def make_prototype_graph():
    G = nx.Graph()
    docs = sm.compute_similarity("../keywords/docs.txt", 2)
    edges_list = []
    nodes_list = []
    for i in docs:
        nodes_list.append(i[0])
        nodes_list.append(i[1])
        edge = (i[0], i[1], {'similarity': docs.get(i)})
        edges_list.append(edge)
    G.add_edges_from(edges_list)
    return G

if __name__ == 'main':
    make_prototype_graph()