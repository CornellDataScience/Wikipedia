import random
import networkx as nx

def DiGraphRandomWalk(G, niters, weight=True):
    # init a random node
    rand_node = random.choice(G.nodes())
    visited_nodes = {}

    if weight == True:
        # run simulation niters times
        for i in range(niters):
            # record current node
            if rand_node in visited_nodes:
                visited_nodes[rand_node] += 1
            else:
                visited_nodes[rand_node] = 1
            # access neighboring nodes
            node_neighbors = G.edges(rand_node, data='weight')
            # make sure neighbors exist
            if len(node_neighbors) == 0:
                break
            # pick a most likely neighbor in terms of edge weight
            sorted_neighbors = sorted(node_neighbors, key=lambda el: el[2], reverse=True)
            # update rand_node for next iteration
            rand_node = sorted_neighbors[0][1]
    else:
        for i in range(niters):
            if rand_node in visited_nodes:
                visited_nodes[rand_node] += 1
            else:
                visited_nodes[rand_node] = 1
            node_neighbors = G.edges(rand_node)
            if len(node_neighbors) == 0:
                break
            rand_node = random.choice(node_neighbors)[1]
    return visited_nodes
