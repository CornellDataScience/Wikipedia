import similarity_new as sn
import randomwalk as rw
import makeGraph as mg
import sys
import json

if __name__ == '__main__':
    scraped_file = sys.argv[1]
    titles, contents = sn.read_data('../data/' + scraped_file)
    doc_term_matrix, vocabulary = sn.preprocess(contents)
    sim_matrix = sn.create_similarity_matrix(doc_term_matrix, vocabulary)
    G = mg.make_prototype_graph(sim_matrix, titles)
    path, graph_path = rw.DiGraphRandomWalk(G, 20, 10, 0, {}, True)
    with open(scraped_file + '_path.json', 'w+') as outfile:
        json.dump(graph_path, outfile)
    weights = []
    for node1, node2 in G.edges():
        weights.append(G[node1][node2]['similarity'])
    n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    plt.show()
