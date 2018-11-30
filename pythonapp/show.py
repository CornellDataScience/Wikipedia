from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Users/Nikhil/Downloads/release/bin'

#dot = Digraph(name='Wikipedia Hierarchy', comment='Created by WikInsite', engine='sfdp', format='png')
def graph(data):
    dot = Digraph(name='Wikipedia Hierarchy', comment='Created by WikInsite', engine='sfdp', format='png')

    dot.attr(size='35,45')

    nodes = []
    for rows in data:
        for title in rows:
            nodes.append(title)
    nodes = list(set(nodes))
    for i in range(len(nodes)):
        dot.node(nodes[i], nodes[i], color='lightblue2', style='filled')

    for rows in data:
        for i in range(len(rows)-1):
            dot.edge(rows[i], rows[i+1], constraint='false')

    dot.render('graph2.gv', view=True)
