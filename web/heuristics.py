import makeGraph as mg
import randomwalk as rw
import matplotlib.pyplot as plt
import random
import networkx as nx
import sys
sys.path.insert(0,'../pythonapp')
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
            G.add_edge(path[n-1],path[n])
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
    # 50 sample random walks for 'Linear algebra' with depth=10 at threshold=0.3 (pre-generated to save time testing)
    # path = [['Linear algebra', 'Norm (mathematics)', 'Function space', 'Dimension (vector space)', 'Space (mathematics)', 'Functional analysis', 'Orthonormal basis', 'Banach space', 'Morphism', 'Function space'], ['Linear algebra', 'Linearization', 'Nonlinear system', 'Eigenvalues and eigenvectors', 'Euclidean vector', 'Norm (mathematics)', 'Banach space', 'Space (mathematics)', 'Functional analysis', 'Topology'], ['Linear algebra', 'Functional analysis', 'Hilbert space', 'Mathematical analysis', 'Mathematical analysis', 'Integral', 'Mathematical analysis', 'Fourier series', 'Mathematical analysis', 'Finite element method'], ['Linear algebra', 'Inner product space', 'Space (mathematics)', 'Norm (mathematics)', 'Functional analysis', 'Functional (mathematics)', 'Equation', 'Finite element method', 'Finite element method', 'Partial differential equation'], ['Linear algebra', 'Dimension (vector space)', 'Euclidean vector', 'Row and column vectors', 'Transformation matrix', 'Transformation matrix', 'Eigenvalues and eigenvectors', 'Nonlinear system', 'Soliton', 'Equation'], ['Linear algebra', 'Function space', 'Norm (mathematics)', 'Hilbert space', 'Calculus of variations', 'Equation', 'Finite element method', 'Partial differential equation', 'Algebraic equation', 'Equation'], ['Linear algebra', 'Three-dimensional space', 'Origin (mathematics)', 'Analytic geometry', 'Geodesic', 'Calculus of variations', 'Function composition', 'Calculus of variations', 'Mathematical analysis', 'Taylor series'], ['Linear algebra', 'Linearization', 'Chaos theory', 'Mathematics', 'Stefan Banach', 'Giuseppe Peano', 'Poland', 'Science', 'Outline of physical science', 'Mathematics'], ['Linear algebra', 'Hilbert space', 'Mathematical analysis', 'Integral equation', 'Algebraic equation', 'Nonlinear system', 'Dynamical system', 'Vector space', 'Scalar (mathematics)', 'Norm (mathematics)'], ['Linear algebra', 'Norm (mathematics)', 'Function space', 'Metric (mathematics)', 'Vector space', 'Functional analysis', 'Linear map', 'Map (mathematics)', 'Higher-order function', 'Calculus of variations'], ['Linear algebra', 'Matrix (mathematics)', 'Row and column vectors', 'Matrix (mathematics)', 'Row and column vectors', 'Sparse matrix', 'Sparse matrix', 'Matrix calculus', 'Row and column vectors', 'Matrix (mathematics)'], ['Linear algebra', 'Linear system', 'Linear system', 'System', 'Dynamical system', 'Vector space', 'Eigenvalues and eigenvectors', 'Function space', 'Topological space', 'Banach space'], ['Linear algebra', 'Vector space', 'Scalar multiplication', 'Scalar multiplication', 'Scalar multiplication', 'Function space', 'Scalar (mathematics)', 'Scalar multiplication', 'Scalar multiplication', 'Vector space'], ['Linear algebra', 'Vector space', 'Norm (mathematics)', 'Functional analysis', 'Norm (mathematics)', 'Vector space', 'Three-dimensional space', 'Hilbert space', 'Vector space', 'Topological space'], ['Linear algebra', 'Dynamical system', 'Linear system', 'Linearization', 'System', 'Linearization', 'Dynamical system', 'Chaos theory', 'Mathematical model', 'System'], ['Linear algebra', 'Functional analysis', 'Space (mathematics)', 'Hilbert space', 'Function space', 'Metric (mathematics)', 'Function space', 'Norm (mathematics)', 'Inner product space', 'Scalar (mathematics)'], ['Linear algebra', 'Banach space', 'Banach space', 'Space (mathematics)', 'Manifold', 'Manifold', 'Geodesic', 'Manifold', 'Surface (topology)', 'Three-dimensional space'], ['Linear algebra', 'Inner product space', 'Scalar (mathematics)', 'Norm (mathematics)', 'Dimension (vector space)', 'Orthonormal basis', 'Banach space', 'Function space', 'Function space', 'Linear map'], ['Linear algebra', 'Linear map', 'Matrix (mathematics)', 'Matrix calculus', 'Vector space', 'Euclidean vector', 'Row and column vectors', 'Sparse matrix', 'Matrix (mathematics)', 'Matrix addition'], ['Linear algebra', 'Banach space', 'Vector space', 'Dynamical system', 'Equation', 'Linearization', 'Linear system', 'Nonlinear system', 'Partial differential equation', 'Finite element method'], ['Linear algebra', 'Row and column vectors', 'Matrix calculus', 'Scalar (mathematics)', 'Inner product space', 'Space (mathematics)', 'Norm (mathematics)', 'Euclidean vector', 'Matrix calculus', 'Row and column vectors'], ['Linear algebra', 'Functional analysis', 'Banach space', 'Continuous function', 'Point (geometry)', 'Origin (mathematics)', 'Origin (mathematics)', 'Line (geometry)', 'Non-Euclidean geometry', 'Axiom'], ['Linear algebra', 'Linear algebra', 'Equation', 'Partial differential equation', 'Nonlinear system', 'Functional (mathematics)', 'Equation', 'Mathematical analysis', 'Calculus of variations', 'Integral'], ['Linear algebra', 'Matrix (mathematics)', 'Invertible matrix', 'Matrix (mathematics)', 'Sparse matrix', 'Invertible matrix', 'Stochastic matrix', 'Sparse matrix', 'Invertible matrix', 'Diagonal matrix'], ['Linear algebra', 'Nonlinear system', 'Algebraic equation', 'Soliton', 'Equation', 'Analytic geometry', 'Origin (mathematics)', 'Line (geometry)', 'Plane (geometry)', 'Space (mathematics)'], ['Linear algebra', 'Linear system', 'Linearization', 'Equation', 'Partial differential equation', 'Integral equation', 'Soliton', 'Soliton', 'Soliton', 'Algebraic equation'], ['Linear algebra', 'Functional analysis', 'Functional analysis', 'Scalar (mathematics)', 'Inner product space', 'Space (mathematics)', 'Function space', 'Endomorphism', 'Group (mathematics)', 'Group (mathematics)'], ['Linear algebra', 'Endomorphism', 'Group (mathematics)', 'Endomorphism', 'Vector space', 'Space (mathematics)', 'Vector space', 'Scalar multiplication', 'Eigenvalues and eigenvectors', 'Rotation matrix'], ['Linear algebra', 'Endomorphism', 'Banach space', 'Orthonormal basis', 'Orthonormal basis', 'Inner product space', 'Inner product space', 'Inner product space', 'Scalar (mathematics)', 'Norm (mathematics)'], ['Linear algebra', 'Banach space', 'Vector space', 'Vector space', 'Functional analysis', 'Hilbert space', 'Mathematical analysis', 'Equation', 'Dynamical system', 'Linearization'], ['Linear algebra', 'Function space', 'Function composition', 'Function composition', 'Morphism', 'Morphism', 'Module homomorphism', 'Endomorphism', 'Module homomorphism', 'Endomorphism'], ['Linear algebra', 'Scalar (mathematics)', 'Euclidean vector', 'Plane (geometry)', 'Affine geometry', 'Euclidean geometry', 'Line (geometry)', 'Two-dimensional space', 'Incidence geometry', 'Linear equation'], ['Linear algebra', 'Linear map', 'Function space', 'Calculus of variations', 'Continuous function', 'Point (geometry)', 'Three-dimensional space', 'Vector space', 'Continuous function', 'Functional (mathematics)'], ['Linear algebra', 'Linear map', 'Linear map', 'Scalar (mathematics)', 'Dimension (vector space)', 'Vector space', 'Linear map', 'Scalar (mathematics)', 'Scalar (mathematics)', 'Dimension (vector space)'], ['Linear algebra', 'Vector space', 'Continuous function', 'Exponential function', 'Calculus of variations', 'Function (mathematics)', 'Point (geometry)', 'Affine geometry', 'Plane (geometry)', 'Space (mathematics)'], ['Linear algebra', 'Orthonormal basis', 'Dimension (vector space)', 'Scalar (mathematics)', 'Inner product space', 'Inner product space', 'Scalar (mathematics)', 'Norm (mathematics)', 'Dimension (vector space)', 'Dimension (vector space)'], ['Linear algebra', 'Linear map', 'Functional analysis', 'Function space', 'Vector space', 'Space (mathematics)', 'Vector space', 'Linear map', 'Function space', 'Scalar (mathematics)'], ['Linear algebra', 'Row and column vectors', 'Matrix calculus', 'Vector space', 'Endomorphism', 'Function composition', 'Function space', 'Endomorphism', 'Module (mathematics)', 'Ring (mathematics)'], ['Linear algebra', 'Eigenvalues and eigenvectors', 'Euclidean vector', 'Orthonormal basis', 'Euclidean vector', 'Dimension (vector space)', 'Space (mathematics)', 'Vector space', 'Row and column vectors', 'Euclidean vector'], ['Linear algebra', 'Nonlinear system', 'Chaos theory', 'Linear system', 'Linearization', 'Linearization', 'Chaos theory', 'Linear system', 'Dynamical system', 'Dynamical system'], ['Linear algebra', 'Dimension (vector space)', 'Space (mathematics)', 'Inner product space', 'Space (mathematics)', 'Banach space', 'Scalar (mathematics)', 'Euclidean vector', 'Plane (geometry)', 'Three-dimensional space'], ['Linear algebra', 'Nonlinear system', 'System', 'System', 'System', 'Nonlinear system', 'Chaos theory', 'Linear system', 'Nonlinear system', 'Eigenvalues and eigenvectors'], ['Linear algebra', 'Linear map', 'Eigenvalues and eigenvectors', 'Equation', 'Linearization', 'Nonlinear system', 'Finite element method', 'Nonlinear system', 'Integral equation', 'Equation'], ['Linear algebra', 'Inner product space', 'Scalar (mathematics)', 'Euclidean vector', 'Three-dimensional space', 'Hilbert space', 'Mathematical analysis', 'Nonlinear system', 'Linear equation', 'Nonlinear system'], ['Linear algebra', 'Transformation matrix', 'Invertible matrix', 'Eigenvalues and eigenvectors', 'Linear map', 'Transformation matrix', 'Matrix (mathematics)', 'Row and column vectors', 'Row and column vectors', 'Transformation matrix'], ['Linear algebra', 'Transformation matrix', 'Linear map', 'Eigenvalues and eigenvectors', 'Diagonal matrix', 'Matrix calculus', 'Invertible matrix', 'Eigenvalues and eigenvectors', 'Matrix calculus', 'Row and column vectors'], ['Linear algebra', 'Vector space', 'Function space', 'Scalar multiplication', 'Vector space', 'Row and column vectors', 'Stochastic matrix', 'Sparse matrix', 'Matrix addition', 'Eigenvalues and eigenvectors'], ['Linear algebra', 'Function space', 'Scalar (mathematics)', 'Matrix calculus', 'Scalar (mathematics)', 'Norm (mathematics)', 'Dimension (vector space)', 'Function space', 'Higher-order function', 'Continuous function'], ['Linear algebra', 'Matrix calculus', 'Eigenvalues and eigenvectors', 'Rotation matrix', 'Matrix (mathematics)', 'Diagonal matrix', 'Matrix addition', 'Matrix addition', 'Matrix (mathematics)', 'Rotation matrix'], ['Linear algebra', 'Plane (geometry)', 'Three-dimensional space', 'Plane (geometry)', 'Euclidean vector', 'Euclidean vector', 'Eigenvalues and eigenvectors', 'Equation', 'Numerical analysis', 'Equation']]

    # # graph with nodes [F,G,H,I] all having distances = diameter
    # G = nx.Graph()
    # G.add_nodes_from(['A','B','C','D','E','F','G','H','I','J','K','L','M'])
    # G.add_edges_from([('A','B'),('A','C'),('A','D'),('A','E'),('B','F'),('C','G'),('E','H'),('D','I'),('F','J'),('J','K'),('K','L'),('G','L'),('G','M'),('M','N'),('O','N'),('H','O'),('H','P'),('Q','P'),('R','Q'),('R','I'),('I','S'),('S','T'),('T','U'),('U','F'),('A','K'),('A','N'),('A','Q'),('A','T')])
    # # graph with max branching (4 unoverlapping branches from node A)
    # G = nx.Graph()
    # G.add_nodes_from(['A','B','C','D','E','F','G','H','I'])
    # G.add_edges_from([('A','B'),('B','C'),('A','D'),('D','E'),('A','F'),('F','G'),('A','H'),('H','I')])
    # # graph with min branching (all nodes connected)
    # G = nx.Graph()
    # G.add_nodes_from(['A','B','C','D','E'])
    # G.add_edges_from([('A','B'),('A','C'),('A','D'),('A','E'),('B','C'),('C','D'),('D','E'),('E','B'),('B','D'),('C','E')])

    G = mg.make_prototype_graph("../data/Linear algebra_2.json").to_directed()
    start_tag = 'Linear algebra'

    loop_vals = []
    branch_vals = []
    # for val in range(1,101):
    path = rw.DiGraphRandomWalk(G, 10, 10, start_tag, True)
    rw_G = make_rw_graph(path)

    print("branch score: {}".format(hyperbolicity(rw_G, 100, 4)))
    print ("loop score: {}".format(loops(path)))
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

    # # dummy data for branching values
    # plt.plot(range(1,101), branch_vals)
    # plt.show()
    # plt.plot(range(1,101), loop_vals)
    # plt.show()
