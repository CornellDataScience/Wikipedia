import random
import networkx as nx
import makeGraph

def DiGraphRandomWalk(G, niters, depth, threshold, weight=True):
    # init a random node
    rand_node = random.choice(G.nodes())
    visited_paths = {}

    if weight == True:
        # run simulation niters times
        for i in range(niters):
            path = {}
            # perform random walk up to specified depth
            for j in range(depth):
                path[j] = rand_node
                count = 0
                # determine successor node
                while True:
                    count = count + 1
                    # end search if no successors exist or if the loop if it has executed (number of neighbors * 50) times
                    if len(G.successors(rand_node)) == 0 or count > len(G.successors(rand_node)) * 50:
                        node_neighbor = "None"
                        break
                    # chooses successor node at random
                    node_neighbor = random.choice(G.successors(rand_node))
                    # leave the loop if an edge within an appropriate threshold is found
                    if G[rand_node][node_neighbor]['weight'] > threshold:
                        break
                # breaks loop if the end of node path has been reached
                if node_neighbor == "None":
                    break
                # update rand_node for next iteration
                rand_node = node_neighbor
            # add the determined path to the list of visited paths
            visited_paths[i] = path
            rand_node = random.choice(G.nodes())
    else:
        # run simulation niters times
        for i in range(niters):
            path = {}
            # perform random walk up to specified depth
            for j in range(depth):
                path[j] = rand_node
                count = 0
                # end search if no successors exist
                if len(G.successors(rand_node)) == 0:
                    break
                # chooses successor node at random
                node_neighbor = random.choice(G.successors(rand_node))
                # update rand_node for next iteration
                rand_node = node_neighbor
            # add the determined path to the list of visited paths
            visited_paths[i] = path
            rand_node = random.choice(G.nodes())
    return visited_paths

if __name__ == '__main__':
    # test scenario
    # G = nx.DiGraph()
    # G.add_nodes_from("abcdefghij")
    # G.add_weighted_edges_from([("a","b", .3),("a","c", .9),("b", "d", .1),("c","e", .1),("c","f", .6),("c","g", .9),("f","h", .6),("g","h", .2),("h","i", .4),("i","j", .6),("d", "i", .3)])

    G = makeGraph.make_prototype_graph().to_directed()
    path = DiGraphRandomWalk(G, 3, 5, .1, False)
    print(path)
