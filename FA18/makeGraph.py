import networkx as nx
# import pandas as pd
import similarity_new as sm
# import pickle
# from gensim import similarities
# makes a graph with edges weights of cosine similarity
# def make_prototype_graph(source):
#     G = nx.Graph()
#     # will reuse similarity weights if they are already computed
#     try:
#         docs = similarities.MatrixSimilarity.load('../data/similarity_matrix_{}.mm'.format(source))
#     except FileNotFoundError:
#         m, d = sm.preprocess(source)
#         docs = sm.create_similarity_matrix(m, d)
#
#     # add all nodes/edges, with similarity values from matrix
#     ridx = 0
#     for r in docs:
#         cidx = ridx
#         for val in r[ridx:]:
#             G.add_edge(ridx,cidx,similarity=val)
#             cidx += 1
#         ridx += 1
#
#     # relabel nodes from indices to article names
#     names = io.open("../data/{}_raw_data.txt".format(source), mode="r", encoding="utf-8", errors="ignore").read().split('\n') # list of strings
#     titles = [names[i] for i in range(len(names)) if i % 2 == 0] # list of string titles
#     mapping = {i:name for i,name in enumerate(titles)}
#
#     G= nx.relabel_nodes(G,mapping)
#
#     return(G.to_directed())

# makes a graph with edges weights of cosine similarity
def make_prototype_graph(matrix, titles):
    G = nx.Graph()
    # add all nodes/edges, with similarity values from matrix
    ridx = 0
    for r in matrix:
        cidx = ridx
        for val in r[ridx:]:
            G.add_edge(ridx,cidx,similarity=val)
            cidx += 1
        ridx += 1

    # # relabel nodes from indices to article names
    # names = io.open("../data/{}_raw_data.txt".format(source), mode="r", encoding="utf-8", errors="ignore").read().split('\n') # list of strings
    # titles = [names[i] for i in range(len(names)) if i % 2 == 0] # list of string titles
    # mapping = {i:name for i,name in enumerate(titles)}

    G= nx.relabel_nodes(G,sm.create_mapping(titles))
    return(G.to_directed())


# if __name__ == 'main':
#     make_prototype_graph("Linear algebra")
