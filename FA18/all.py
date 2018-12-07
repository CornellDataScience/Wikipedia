import scraper_new as sc
import similarity_new as sm
import randomwalk as rw
import makeGraph as mg
import sys
import json
import matplotlib.pyplot as plt
import random


def all(root_page, downstream):
    # STEP 1: scrape Wikipedia pages
    page_title = root_page.split("/")[-1]
    # links = sc.get_links(root_page)
    # titles_dict = sc.read_pages(links, page_title)

    # Uncomment the following if sorting is needed:
    # titles_dict = sorted(titles_dict.items(), key=lambda x: x[1], reverse=True)

    # STEP 2: create similarity matrix between articles
    # titles, contents = sm.read_data('../data/' + page_title + '_raw_data.txt')
    titles, contents = sm.read_data('../topic_modeling_wikipedia/raw_data.txt')
    doc_term_matrix, vocabulary = sm.preprocess(contents)
    sim_matrix = sm.create_similarity_matrix(doc_term_matrix, vocabulary)

    # STEP 3: create graph weighted with similarity values
    G = mg.make_prototype_graph(sim_matrix, titles)
    # STEP 4: perform random walk
    dummy_inlinks = {}  # TODO: replace with actual inlinks
    for n in G.nodes():
        dummy_inlinks[n] = random.randint(1, 10)
    path, graph_path = rw.DiGraphRandomWalk(G, 10, 10, 'Linear algebra', dummy_inlinks, downstream)
    # with open(page_title + '_path.json', 'w+') as outfile:
    #     json.dump(graph_path, outfile)
    weights = []
    for node1, node2 in G.edges():
        weights.append(G[node1][node2]['similarity'])
    n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    plt.show()

    return path


if __name__ == '__main__':
    print(all('https://en.wikipedia.org/wiki/Linear_algebra', True))
