import networkx as nx
import pandas as pd
import similarity as sm

#makes a graph based on the original format of the data, with depth 1
#mainly to provide data for random walks
def make_prototype_graph():
    G = nx.Graph()
    docs = sm.compute_similarity("../keywords/linalg_desclinks.json")
    G.add_edges_from(docs)
    return G

if __name__ == 'main':
    make_prototype_graph()
