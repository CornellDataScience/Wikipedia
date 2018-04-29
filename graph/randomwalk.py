import random
import networkx as nx
import makeGraph
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def DiGraphRandomWalk(G, niters, depth, threshold, weight=True):
    # init a random node
    rand_node = G.nodes()[random.randint(0, len(G.nodes()))]
    #for i in G.nodes():
    #    if i == start_tag:
    #        start_node = i
    #rand_node = start_node
    visited_paths = []

    if weight == True:
        # run simulation niters times
        for i in range(niters):
            path = []
            # perform random walk up to specified depth
            for j in range(depth):
                path.append(rand_node)
                count = 0
                # determine successor node
                while True:
                    count = count + 1
                    # end search if no successors exist or if the loop if it has executed (number of successors * 50) times
                    if len(G.successors(rand_node)) == 0 or count > len(G.successors(rand_node)) * 50:
                        node_neighbor = "None"
                        break
                    # chooses successor node at random
                    node_neighbor = random.choice(G.successors(rand_node))
                    # leave the loop if an edge within an appropriate threshold is found
                    print ("randnode: ", G.node[rand_node]['pagerank'], " <= nodeneighbor: ", G.node[node_neighbor]['pagerank'])
                #    if G[rand_node][node_neighbor]['similarity'] > threshold:
                #        print ("Similarity good")
                #    else:
                #        print ("Similarity bad")
                    if G[rand_node][node_neighbor]['similarity'] > threshold and G.node[node_neighbor]['pagerank'] >= G.node[rand_node]['pagerank']:
                #        print ("Success")
                        break
                # breaks loop if the end of node path has been reached
                if node_neighbor == "None":
                    break
                # update rand_node for next iteration
                rand_node = node_neighbor
            # add the determined path to the list of visited paths
            visited_paths.append(path)
            rand_node = G.nodes()[random.randint(0, len(G.nodes()))]
    else:
        # run simulation niters times
        for i in range(niters):
            path = []
            # perform random walk up to specified depth
            for j in range(depth):
                path.append(rand_node)
                # end search if no successors exist
                if len(G.successors(rand_node)) == 0:
                    break
                # chooses successor node at random
                node_neighbor = random.choice(G.successors(rand_node))
                # update rand_node for next iteration
                rand_node = node_neighbor
            # add the determined path to the list of visited paths
            visited_paths.append(path)
            rand_node = G.nodes()[random.randint(0, len(G.nodes()))]
    return visited_paths

if __name__ == '__main__':
    # test scenario
    # G = nx.DiGraph()
    # G.add_nodes_from("abcdefghij")
    # G.add_weighted_edges_from([("a","b", .3),("a","c", .9),("b", "d", .1),("c","e", .1),("c","f", .6),("c","g", .9),("f","h", .6),("g","h", .2),("h","i", .4),("i","j", .6),("d", "i", .3)])

    # obtain graph of articles and perform random walks
    G = makeGraph.make_prototype_graph().to_directed()
    path = DiGraphRandomWalk(G, 20, 10, 0.2, True)
    # output paths taken
    print(path)
    # generate list of edge weights
    weights = []
    for node1, node2 in G.edges():
        weights.append(G[node1][node2]['similarity'])
    # Display histogram of cosine similarity values
    n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    plt.show()
