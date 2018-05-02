import networkx as nx
import pandas as pd
import similarity as sm

#makes a graph based on the original format of the data, with depth 1
#mainly to provide data for random walks
def make_prototype_graph(source):
    G = nx.Graph()
    docs = sm.compute_similarity(source)
    G.add_edges_from(docs)
    pr = nx.pagerank(G)
    nx.set_node_attributes(G, pr,"pagerank")
    return G

if __name__ == 'main':
    make_prototype_graph()
