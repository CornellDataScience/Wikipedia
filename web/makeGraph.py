import networkx as nx
import similarity_new as sm
import pickle
import io


# makes a graph with nodes attribute is pagerank
# and edges weights are cosine similarity
def make_prototype_graph(source):
    G = nx.Graph()
    # will reuse similarity weights if they are already computed
    try:
        docs = io.open("similarity_matrix_{}.mm".format(source[:-3]), mode="r", encoding="utf-8", errors="ignore").read()
    except FileNotFoundError:
        docs = sm.create_similarity_matrix(preprocess(source))
    # m,d = sm.preprocess(source)
    # docs = sm.create_similarity_matrix(m,d)
    G.add_edges_from(docs)
    pr = nx.pagerank(G)
    nx.set_node_attributes(G, pr, "pagerank")
    return G


if __name__ == 'main':
    make_prototype_graph("Linear algebra")
