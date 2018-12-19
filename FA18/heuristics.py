import makeGraph as mg
import randomwalk as rw
import matplotlib.pyplot as plt
import random
import networkx as nx
import sys
sys.path.insert(0, '../pythonapp')
import show

'''
Returns a value representing the degree of branching of a network graph.
An amount of nodes, based on degree, are randomly selected niters times and
the shortest distances between all nodes is found and averaged.
The value is normalized by niters and the amount of degree matches.
TODO: find factor to normalize to 0 to 1 (currently using graph diameter)
'''
def hyperbolicity(G, niters, degree):
    total_dist_sum = 0
    for i in range(niters):
        try:
            nodes = random.sample(nx.nodes(G), degree)
        except ValueError:
            return 0
        dist_sum = 0
        for n in range(len(nodes)):
            for n1 in range(len(nodes))[(n+1):]:
                dist_sum += nx.shortest_path_length(G, nodes[n], nodes[n1])
        total_dist_sum += dist_sum
    return(total_dist_sum/(niters*((degree*(degree-1))/2)))


'''
Converts random walk output into a networkx graph.
'''
def make_rw_graph(paths):
    # # generate a directed graph graphic
    # dG = nx.DiGraph()
    # for path in paths:
    #     dG.add_nodes_from(path)
    #     for n in range(len(path))[1:]:
    #         dG.add_edge(path[n-1],path[n])
    # nx.draw_networkx(dG)
    # plt.show()
    G = nx.Graph()
    for path in paths:
        G.add_nodes_from(path)
        for n in range(len(path))[1:]:
            G.add_edge(path[n-1], path[n])
    return(G)


'''
Returns a value representing the average degree of loop occurence in a set of random walks.
Subvalues are calculated for each loop, calculated by subtracting the distance between the nodes from the length of the path.
This gives larger loops a smaller value and smaller loops a higher value.
Total value = (sum of subvalues)/(# of walks)/(max possible total value)
The sum is divided by the # of walks to get the average value per walk.
Then it is divided by the max possible value, which graph [a, a, a, ...].
This normalizes score such that a 1.0 indicates only self loops, and 0.0 indicates no loops.

e.g.
list = (A) -> (B) -> (C) -> (C) -> (A) -> (D) -> (A)
1) loop from [2] to [3], value = (list length)-(distance between loop) = 7-1 = 6
2) loop from [0] to [4], value = 7-4 = 3
3) loop from [4] to [6], value = 7-2 = 5
4) loop from [0] to [6], value = 7-6 = 1
Total value = (sum of subvalues)/(# of walks)/(max possible total value)
            = 15/1/[(6)+(6+5)+(6+5+4)+...+(6+5+4+3+2+1)]
            = 0.0002996
'''
def loops(visited_paths):
    score = 0
    depth = len(visited_paths[0])
    for path in visited_paths:
        path = list(enumerate(path))
        for i,e in path[1:]:
            for i1,e1 in path[:i]:
                if e1 == e:
                    score += depth-(i-i1)
    try:
        return score/len(visited_paths)/sum([i**2 for i in range(depth-1, 0, -1)])
    except ZeroDivisionError:
        return 0


'''
Same as loops except outputted value is higher for larger loops. Do not use.
'''
def loops_old(visited_paths):
    score = 0
    for path in visited_paths:
        path = list(enumerate(path))
        for i,e in path[1:]:
            for i1,e1 in path[:i]:
                if e1 == e:
                    score += i-i1
    try:
        return score/len(visited_paths)/sum([i*(i+1)/2 for i in range(1, len(visited_paths[0]))])
    except ZeroDivisionError:
        return 0


if __name__ == '__main__':
    # # graph with nodes [F,G,H,I] all having distances = diameter
    # G = nx.Graph()
    # G.add_nodes_from(['A','B','C','D','E','F','G','H','I','J','K','L','M'])
    # G.add_edges_from([('A','B'),('A','C'),('A','D'),('A','E'),('B','F'),('C','G'),('E','H'),('D','I'),('F','J'),('J','K'),('K','L'),('G','L'),('G','M'),('M','N'),('O','N'),('H','O'),('H','P'),('Q','P'),('R','Q'),('R','I'),('I','S'),('S','T'),('T','U'),('U','F'),('A','K'),('A','N'),('A','Q'),('A','T')])
    # graph with max branching (4 unoverlapping branches from node A)
    # G = nx.Graph()
    # G.add_nodes_from(['A','B','C','D','E','F','G','H','I'])
    # G.add_edges_from([('A','B'),('B','C'),('A','D'),('D','E'),('A','F'),('F','G'),('A','H'),('H','I')])
    # # graph with min branching (all nodes connected)
    # G = nx.Graph()
    # G.add_nodes_from(['A','B','C','D','E'])
    # G.add_edges_from([('A','B'),('A','C'),('A','D'),('A','E'),('B','C'),('C','D'),('D','E'),('E','B'),('B','D'),('C','E')])
    # bipartite graph K4,4
    # G = nx.Graph()
    # G.add_nodes_from(['a1','a2','a3','a4','b1','b2','b3','b4'])
    # G.add_edges_from([('a1','b1'),('a1','b2'),('a1','b3'),('a1','b4'),('a2','b1'),('a2','b2'),('a2','b3'),('a2','b4'),('a3','b1'),('a3','b2'),('a3','b3'),('a3','b4'),('a4','b1'),('a4','b2'),('a4','b3'),('a4','b4')])
    G = mg.make_prototype_graph("../data/Linear algebra_2.json").to_directed()
    start_tag = 'Linear algebra'

    loop_vals = []
    branch_vals = []
    for val in range(2,101):
        path = rw.DiGraphRandomWalk(G, val, 10, start_tag, True)
        rw_G = make_rw_graph(path)
        constant = rw_G.number_of_edges()/(rw_G.number_of_nodes()-1)
    # print(constant)
        print("branch score: {}".format(constant))
        branch_vals.append(constant)
    # print ("loop score: {}".format(loops(path)))
    show.graph(path)

        # avg_loop_count = 0
        # avg_branch_count = 0
        # for i in range(1,51):
        #     avg_loop_count += loops(path)
        #     avg_branch_count += hyperbolicity(rw_G, 100, 4)
        # avg_loop_count /= 50
        # avg_branch_count /= 50
        # loop_vals.append(avg_loop_count)
        # branch_vals.append(avg_branch_count)

    # dummy data for branching values
    plt.plot(range(2,101), branch_vals)
    plt.show()
    # plt.plot(range(1,101), loop_vals)
    # plt.show()
