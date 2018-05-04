import networkx as nx
import pandas as pd
import similarity as sm

#makes a graph with nodes attribute is pagerank
#   and edges weights are cosine similarity
def make_prototype_graph(source):
    G = nx.Graph()
    docs = sm.compute_similarity(source)
    G.add_edges_from(docs)
    pr = nx.pagerank(G)
    nx.set_node_attributes(G, pr,"pagerank")
    return G

if __name__ == 'main':
    make_prototype_graph()
