import random

def DiGraphRandomWalk(G, niters, depth, threshold, start_tag, weight=True):
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
                    if G[rand_node][node_neighbor]['similarity'] > threshold:
                        break
                # breaks loop if the end of node path has been reached
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
                if len(G.successors(rand_node)) == 0:
                    break
                # chooses successor node at random
                node_neighbor = random.choice(G.successors(rand_node))
                # update rand_node for next iteration
                rand_node = node_neighbor
            # add the determined path to the list of visited paths
            visited_paths.append(path)
            rand_node = start_node
    return visited_paths
