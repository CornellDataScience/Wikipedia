import networkx as nx
import pandas as pd
import similarity_new as sm
import pickle
from gensim import similarities
# makes a graph with nodes attribute is pagerank
# and edges weights are cosine similarity
def make_prototype_graph(source):
    G = nx.Graph()
    # will reuse similarity weights if they are already computed
    try:
        docs = similarities.MatrixSimilarity.load('./similarity_matrix.mm')
        # with open("{}_similarity.txt".format(source[:-5]), 'rb') as file:
        #     docs = pickle.load(file)
    except FileNotFoundError:
        m, d = sm.preprocess(source)
        docs = sm.create_similarity_matrix(m, d)

    G.add_edges_from(docs)
    pr = nx.pagerank(G)
    nx.set_node_attributes(G, pr, "pagerank")
    return G

if __name__ == 'main':
    make_prototype_graph()
