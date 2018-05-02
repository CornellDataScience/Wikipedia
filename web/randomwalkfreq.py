import random
import networkx as nx
import makeGraph
import numpy as np
import operator
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def DiGraphRandomWalk(G, niters, depth, threshold, start_tag, weight=True):
    # init with node matching start_tag
    for i in G.nodes():
        if i == start_tag:
            start_node = i
    rand_node = start_node
    # create list of dictionaries containing the freq of nodes at each step
    dict_list = []
    for d in range(depth):
        dict_list.append({})

    # run weighted random walk
    if weight == True:
        # run simulation niters times
        for i in range(niters):
            # perform random walk up to specified depth
            for j in range(depth):
                # add/increment current node to the appropriate dictionary
                if rand_node in dict_list[j]:
                    dict_list[j][rand_node] += 1
                else:
                    dict_list[j][rand_node] = 1
                count = 0
                # determine successor node
                while True:
                    count = count + 1
                    # end search if no successors exist or if the loop has executed (number of successors * 50) times
                    if len(list(G.successors(rand_node))) == 0 or count > len(list(G.successors(rand_node))) * 50:
                        node_neighbor = "None"
                        break
                    # choose successor node at random
                    node_neighbor = random.choice(list(G.successors(rand_node)))
                    # leave the loop if an edge within an appropriate threshold is found and successor node has a higher or equal PageRank
                    if G[rand_node][node_neighbor]['similarity'] > threshold and G.node[node_neighbor]['pagerank'] >= G.node[rand_node]['pagerank']:
                        break
                # break loop if the end of node path has been reached
                if node_neighbor == "None":
                    break
                # update rand_node for next iteration
                rand_node = node_neighbor
            # reset random walk starting node for next iteration
            rand_node = start_node
    # run unweighted random walk
    else:
        # run simulation niters times
        for i in range(niters):
            # perform random walk up to specified depth
            for j in range(depth):
                # add/increment current node to the appropriate dictionary
                if rand_node in dict_list[j]:
                    dict_list[j][rand_node] += 1
                else:
                    dict_list[j][rand_node] = 1
                # end search if no successors exist
                if len(list(G.successors(rand_node))) == 0:
                    break
                # choose successor node at random
                node_neighbor = random.choice(list(G.successors(rand_node)))
                # update rand_node for next iteration
                rand_node = node_neighbor
            # reset random walk starting node for next iteration
            rand_node = start_node
    # filter dictionaries to contain the 3 most frequent nodes at each step
    for d in range(depth):
        dict_list[d] = dict(sorted(dict_list[d].items(), key=operator.itemgetter(1), reverse=True)[:3])
    return dict_list

if __name__ == '__main__':
    # obtain graph of articles and perform random walks
    G = makeGraph.make_prototype_graph().to_directed()
    freqs = DiGraphRandomWalk(G, 100, 5, 0.3, 'Linear algebra', False)
    # output list of frequencies
    print(freqs)

    # generate list of edge weights
    # weights = []
    # for node1, node2 in G.edges():
    #     weights.append(G[node1][node2]['similarity'])
    # Display histogram of cosine similarity values
    # n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    # plt.show()
