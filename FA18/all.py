import scraper_new as sc
import similarity_new as sm
import randomwalk as rw
import makeGraph as mg
import sys
import json

if __name__ == '__main__':
    root_page = sys.argv[1]
    page_title = root_page.split("/")[-1]
    links = sc.get_links(root_page)
    titles_dict = sc.read_pages(links, page_title)
    # Uncomment the following if sorting is needed:
    # titles_dict = sorted(titles_dict.items(), key=lambda x: x[1], reverse=True)
    titles, contents = sm.read_data('../data/' + page_title + '_raw_data.txt')
    doc_term_matrix, vocabulary = sm.preprocess(contents)
    clusters = sm.cluster(doc_term_matrix, 15, vocabulary)
    print(clusters)
    sim_matrix = sm.create_similarity_matrix(doc_term_matrix, vocabulary)
    G = mg.make_prototype_graph(sim_matrix, titles)
    path, graph_path = rw.DiGraphRandomWalk(G, 20, 10, 0, {}, True)
    with open(scraped_file + '_path.json', 'w+') as outfile:
        json.dump(graph_path, outfile)
    weights = []
    for node1, node2 in G.edges():
        weights.append(G[node1][node2]['similarity'])
    n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    plt.show()
