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

import json

def DiGraphRandomWalk(G, niters, depth, start_tag, inlinks, downstream):
    graph_path = {"nodes":[], "links":[]}
    # init a random node
    id = 0;
    node_id = {}
    for i in G.nodes():
        graph_path["nodes"].append({"name":i, "id":id, "paths":[]})
        node_id[i] = id
        id = id + 1
        if i == start_tag:
            start_node = i
    rand_node = start_node
    visited_paths = []


    # run simulation niters times
    for i in range(niters):
        path = []
        # perform random walk up to specified depth
        for j in range(depth):
            rand_node_paths = graph_path["nodes"][node_id[rand_node]]["paths"]
            rand_node_paths.append(i) if (not (i in rand_node_paths)) else ""

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

            # Weighted Randomization code
            totals = []
            running_total = 0

            for k in edges_threshold.keys():
                running_total += k
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
                # if G.node[node_neighbor]['pagerank'] >= G.node[rand_node]['pagerank']:
                if inlinks[rand_node] >= inlinks[node_neighbor]:
                    if downstream:
                        graph_path["links"].append({"source":node_id[rand_node], "target":node_id[node_neighbor], "path":i, "step":j, "similarity":G[rand_node][node_neighbor]['similarity']})
                        break
                else:
                    if upstream:
                        graph_path["links"].append({"source":node_id[rand_node], "target":node_id[node_neighbor], "path":i, "step":j, "similarity":G[rand_node][node_neighbor]['similarity']})
                        break

            if node_neighbor == "None":
                break
            # update rand_node for next iteration
            rand_node = node_neighbor

        rand_node_paths = graph_path["nodes"][node_id[rand_node]]["paths"]
        rand_node_paths.append(i) if (not (i in rand_node_paths)) else ""

        # add the determined path to the list of visited paths
        visited_paths.append(path)
        rand_node = start_node

    return visited_paths, graph_path


if __name__ == '__main__':

    G = mg.make_prototype_graph("Linear_algebra")
    # set last parameter to True if going downstream, False if upstream
    path, graph_path = DiGraphRandomWalk(G, 20, 10, 0, {}, True) #TODO: find actual start node

    print(path)
    with open("Linear_algebra_path.json", "w") as outfile:
        json.dump(graph_path, outfile)

    # show.graph(path)

    # generate list of edge weights
    # weights = []
    # for node1, node2 in G.edges():
    #     weights.append(G[node1][node2]['similarity'])
    # # Display histogram of cosine similarity values
    # n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    # plt.show()
