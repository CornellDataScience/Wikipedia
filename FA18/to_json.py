import all


''' Converts random walk lists and cluster data into json format. '''
def store_paths(paths, clusters):
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
        for c in range(len(clusters)):
            if n in clusters[c]:
                node['cluster'] = c
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
    # paths = [['Hevea brasiliensis', 'Angle', 'Tabebuia ochracea', 'Kielmeyera coriacea', 'Avocado', 'Brazil', 'Avocado', 'Brazil', 'Ormosia nobilis', 'Heah Joo Seang'], ['Hevea brasiliensis', 'Henry Wickham (explorer)', 'Hymenaea courbaril', 'Amazon rubber boom', 'Mesoamerican ballgame', 'Malaysia', 'Mesoamerican ballgame', 'Spondias mombin', 'Malaysia', 'Brazil'], ['Hevea brasiliensis', 'Avocado', 'Manaus', 'Angle', 'Attalea maripa', 'Brazil', 'Tabebuia ochracea', 'Malaysia', 'Attalea maripa', 'Manaus'], ['Hevea brasiliensis', 'South Asia', 'Henry Wickham (explorer)', 'South Asia', 'Pouteria caimito', 'Copernicia prunifera', 'Attalea maripa', 'Angle', 'Copernicia prunifera', 'Attalea maripa'], ['Hevea brasiliensis', 'Tabebuia ochracea', 'Avocado', 'Tabebuia ochracea', 'Avocado', 'Tabebuia ochracea', 'Manaus', 'Spondias mombin', 'Kielmeyera coriacea', 'Manaus'], ['Hevea brasiliensis', 'Copernicia prunifera', 'Manaus', 'Copernicia prunifera', 'Angle', 'Tabebuia ochracea', 'Ormosia nobilis', 'Avocado', 'Pouteria caimito', 'Brazil'], ['Hevea brasiliensis', 'Amazon rubber boom', 'Manaus', 'Angle', 'Clusia alata', 'Natural rubber', 'Brazil', 'Tabebuia ochracea', 'India', 'Manaus'], ['Hevea brasiliensis', 'South Asia', 'Clusia alata', 'Potato', 'Angle', 'Pouteria caimito', 'Clusia alata', 'Anadenanthera peregrina var. falcata', 'Natural rubber', 'Hymenaea courbaril'], ['Hevea brasiliensis', 'Brazil', 'Tabebuia ochracea', 'Anadenanthera peregrina var. falcata', 'Avocado', 'Pouteria caimito', 'Brazil', 'Spondias mombin', 'Malaysia', 'Pouteria caimito'], ['Hevea brasiliensis', 'Hymenaea courbaril', 'Attalea maripa', 'Brazil', 'Avocado', 'Brazil', 'Amazon rubber boom', 'Brazil', 'Copernicia prunifera', 'Potato']]

    paths, clusters = all.all('https://en.wikipedia.org/wiki/Linear_algebra', True)
    print(store_paths(paths, clusters))
