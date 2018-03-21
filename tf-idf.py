"""
A module to implement term frequency-inverse document frequency matrix
"""

def doc_to_vec(term_list):
    d = {}
    for v in terms:
        d[v] = term_list.count(v)
    return d

def query_to_vec(term_list):
    d = {}
    for v in terms:
        d[v] = term_list.count(v)
    return d
