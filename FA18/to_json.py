import json
import random

''' Converts random walk lists and cluster data into json format. '''
def store_paths(paths):
    inlinks = {}
    dataset = {}
    nodelist = []
    edgelist = []
    edges = []
    # get nodes and edges from randomwalk paths
    for path in paths:
        for e in range(len(path)):
            nodelist.append(path[e])
            if e != 0:
                edges.append((path[e-1], path[e]))
                if path[e] in inlinks:
                    inlinks[path[e]] += 1
                else:
                    inlinks[path[e]] = 1

    # get rid of duplicate nodes, create dictionary with node ids
    nodeskey = dict([(val, idx) for idx, val in (enumerate(list(set(nodelist))))])
    nodelist = []
    for n in nodeskey.keys():
        node = {}
        node['name'] = n
        node['cluster'] = random.randint(0, 9)  # TODO: update cluster
        if n in inlinks:
            node['inlinks'] = inlinks[n]
        else:
            node['inlinks'] = 0
        nodelist.append(node)

    # remove and count duplicate edges
    nondupedges = []
    iters = {}
    for x in edges:
        if x not in iters:
            iters[x] = 1
            nondupedges.append(x)
        else:
            iters[x] += 1
    # create edge dictionary objects
    count = 0
    for x, y in nondupedges:
        edge = {}
        edge['id'] = count
        edge['source'] = nodeskey[x]
        edge['target'] = nodeskey[y]
        edge['iters'] = iters[(x, y)]
        edgelist.append(edge)
        count += 1

    dataset['nodes'] = nodelist
    dataset['edges'] = edgelist

    return dataset


if __name__ == '__main__':
    paths = [['Linear algebra', 'Norm (mathematics)', 'Function space', 'Dimension (vector space)', 'Space (mathematics)', 'Functional analysis', 'Orthonormal basis', 'Banach space', 'Morphism', 'Function space'], ['Linear algebra', 'Linearization', 'Nonlinear system', 'Eigenvalues and eigenvectors', 'Euclidean vector', 'Norm (mathematics)', 'Banach space', 'Space (mathematics)', 'Functional analysis', 'Topology'], ['Linear algebra', 'Functional analysis', 'Hilbert space', 'Mathematical analysis', 'Mathematical analysis', 'Integral', 'Mathematical analysis', 'Fourier series', 'Mathematical analysis', 'Finite element method'], ['Linear algebra', 'Inner product space', 'Space (mathematics)', 'Norm (mathematics)', 'Functional analysis', 'Functional (mathematics)', 'Equation', 'Finite element method', 'Finite element method', 'Partial differential equation'], ['Linear algebra', 'Dimension (vector space)', 'Euclidean vector', 'Row and column vectors', 'Transformation matrix', 'Transformation matrix', 'Eigenvalues and eigenvectors', 'Nonlinear system', 'Soliton', 'Equation'], ['Linear algebra', 'Function space', 'Norm (mathematics)', 'Hilbert space', 'Calculus of variations', 'Equation', 'Finite element method', 'Partial differential equation', 'Algebraic equation', 'Equation'], ['Linear algebra', 'Three-dimensional space', 'Origin (mathematics)', 'Analytic geometry', 'Geodesic', 'Calculus of variations', 'Function composition', 'Calculus of variations', 'Mathematical analysis', 'Taylor series'], ['Linear algebra', 'Linearization', 'Chaos theory', 'Mathematics', 'Stefan Banach', 'Giuseppe Peano', 'Poland', 'Science', 'Outline of physical science', 'Mathematics'], ['Linear algebra', 'Hilbert space', 'Mathematical analysis', 'Integral equation', 'Algebraic equation', 'Nonlinear system', 'Dynamical system', 'Vector space', 'Scalar (mathematics)', 'Norm (mathematics)'], ['Linear algebra', 'Norm (mathematics)', 'Function space', 'Metric (mathematics)', 'Vector space', 'Functional analysis', 'Linear map', 'Map (mathematics)', 'Higher-order function', 'Calculus of variations']]

    print(store_paths(paths))
