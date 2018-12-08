import scraper_new as sc
import similarity_new as sm
import randomwalk as rw
import makeGraph as mg
import pickle


def all(root_page, downstream):
    # STEP 1: scrape Wikipedia pages
    page_title = root_page.split("/")[-1]
    # if raw data already exists, skip scraping
    try:
        with open("../data/" + page_title + '_dict.txt', 'rb') as f:
            titles_dict = pickle.load(f)
    except:
        links = sc.get_links(root_page)
        titles_dict = sc.read_pages(links, page_title)

    # # Uncomment the following if sorting is needed:
    # titles_dict = sorted(titles_dict.items(), key=lambda x: x[1], reverse=True)

    # STEP 2: create similarity matrix between articles
    titles, contents = sm.read_data('../data/' + page_title + '_raw_data.txt')

    # update inlink dictionary to indicate articles that have 0 inlinks
    for article in (set(titles)-set(titles_dict.keys())):
        titles_dict[article] = 0

    doc_term_matrix, vocabulary = sm.preprocess(contents)
    clusters = sm.cluster(doc_term_matrix, 15, vocabulary, titles)
    sim_matrix = sm.create_similarity_matrix(doc_term_matrix, vocabulary)

    # STEP 3: perform random walk
    G = mg.make_prototype_graph(sim_matrix, titles)
    path, graph_path = rw.DiGraphRandomWalk(G, 10, 10, page_title.replace("_", " "), titles_dict, downstream)

    return path, clusters


if __name__ == '__main__':
    print(all('https://en.wikipedia.org/wiki/Hevea_brasiliensis', True))
