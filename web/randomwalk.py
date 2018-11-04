from bisect import bisect_right
import random
import networkx as nx
import makeGraph as mg
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,'../pythonapp')
import show

def DiGraphRandomWalk(G, niters, depth, start_tag, weight=True):
    # init a random node
    for i in G.nodes():
        if i == start_tag:
            start_node = i
    rand_node = start_node
    visited_paths = []

    if weight == True:
        # run simulation niters times
        for i in range(niters):
            path = []
            # perform random walk up to specified depth
            for j in range(depth):
                #automated threshold value
                edges_nodes = {}
                for node2 in G.successors(rand_node):
                    edges_nodes[G[rand_node][node2]['similarity']] = node2
                #filter all values of 1 from list
                edges_nodes = {k:v for (k,v) in edges_nodes.items() if k < 0.99998}
                #max value
                max_edge = max(list(edges_nodes.keys()))
                threshold = max_edge * 0.1
                #finding all edges above the threshold
                edges_threshold = {k:v for (k,v) in edges_nodes.items() if k >= threshold}

                # Debugging
                # print("Node: " + rand_node)
                # for i in list(edges_threshold.keys()):
                    # print(i)

                # Weighted Randomization code
                totals = []
                running_total = 0

                for i in edges_threshold.keys():
                    running_total += i
                    totals.append(running_total)


                path.append(rand_node)
                count = 0

                while True:
                    count = count + 1
                    rand = random.random() * running_total
                    rand_edge = list(edges_threshold.keys())[bisect_right(totals, rand)]
                    node_neighbor = edges_threshold.get(rand_edge)
                    if len(list(G.successors(rand_node))) == 0 or count > len(list(G.successors(rand_node))) * 50:
                        node_neighbor = "None"
                        break
                    if G.node[node_neighbor]['pagerank'] >= G.node[rand_node]['pagerank']:
                        break

                # determine successor node
                # while True:
                #     count = count + 1
                #     # end search if no successors exist or if the loop has executed (number of successors * 50) times
                #     if len(list(G.successors(rand_node))) == 0 or count > len(list(G.successors(rand_node))) * 50:
                #         node_neighbor = "None"
                #         break
                #     # chooses successor node at random
                #     node_neighbor = random.choice(list(G.successors(rand_node)))
                #     # leave the loop if an edge within an appropriate threshold is found and successor node has a higher or equal PageRank
                #     if G[rand_node][node_neighbor]['similarity'] > threshold and G.node[node_neighbor]['pagerank'] >= G.node[rand_node]['pagerank']:
                #         break
                # # breaks loop if the end of node path has been reached
                if node_neighbor == "None":
                    break
                # update rand_node for next iteration
                rand_node = node_neighbor
            # add the determined path to the list of visited paths
            visited_paths.append(path)
            rand_node = start_node
    else:
        # run simulation niters times
        for i in range(niters):
            path = []
            # perform random walk up to specified depth
            for j in range(depth):
                path.append(rand_node)
                # end search if no successors exist
                if len(list(G.successors(rand_node))) == 0:
                    break
                # chooses successor node at random
                node_neighbor = random.choice(list(G.successors(rand_node)))
                # update rand_node for next iteration
                rand_node = node_neighbor
            # add the determined path to the list of visited paths
            visited_paths.append(path)
            rand_node = start_node
    return visited_paths

if __name__ == '__main__':
    # obtain graph of articles and perform random walks
    G = mg.make_prototype_graph("../data/Linear algebra_2.json").to_directed()
    path = DiGraphRandomWalk(G, 20, 10, 'Linear algebra', True)
    # output paths taken
    print(path)

    show.graph(path)

    # generate list of edge weights
    # weights = []
    # for node1, node2 in G.edges():
    #     weights.append(G[node1][node2]['similarity'])
    # # Display histogram of cosine similarity values
    # n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    # plt.show()
