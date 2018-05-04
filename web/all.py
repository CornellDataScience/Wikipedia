import sys
import json
import randomwalk as rw
import scrape_json as scrape
import similarity as sm
import makeGraph as mg
import randomwalkfreq as rwf
import matplotlib.pyplot as plt

NUM_ITERATIONS = 20 #NUMBER OF ITERATIONS OF RANDOM WALK
DEPTH = 10 #NUMBER OF STEPS TO TAKE IN RANDOM WALK

# generates a graph of the similarity values across documents
# G: a graph generated with networkx, with nodes as artilces and edges
#   the cosine similarity between therm
def plot_similarity(G):
    weights = []
    for node1, node2 in G.edges():
        weights.append(G[node1][node2]['similarity'])
    # Display histogram of cosine similarity values
    n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    plt.show()

# builds a dictionary that is an element of the final list used on the front end
# level: the "step" in the random walk to consider, ie. which dictionary in
#   data to consider (see below)
# data: the paths list to consider. this list is generated by the randomwalkfreq
#   script and has the overall structure:
#       [{"children":[...]},{"children":[...]}]
def build_dict(level, data):
    topics= {}
    topics["children"] =[]
    title = ""
    freq = 0
    url = ""
    desc = ""
    for k in path[level].keys():
        for d in data["pages"]:
            if d["title"] == k:
                url = d["url"]
                desc = d["desc_text"]
        freq = path[level].get(k)
        info_dict = {"title": k, "url": url, "desc": desc, "freq": freq}
        topics["children"].append(info_dict)
    return topics

# depth: the number of child articles to take links from [1,2]
# root_page: the link to the wikipedia article
if __name__ == '__main__':
    depth = int(sys.argv[1])
    root_page = str(sys.argv[2])
    print("depth: " + str(depth))
    print("root page: " +root_page)
    # if you've already scraped and have a file, comment out lines 56-59
    # to decrease runtime
    if depth == 1:
        t = scrape.desc_1(root_page)
    elif depth == 2:
        t = scrape.desc_2(root_page)
    doc_title = "../data/" + root_page[30:]+ "_"+str(depth)+".json"
    print("***** saved to file " + doc_title)

    # make the Graph where edges weighted by cosine similarity
    # and nodes have their pagerank as an attribute
    print("***** finding similarity and pagerank")
    G = mg.make_prototype_graph(doc_title).to_directed()
    with open(doc_title, "r") as f:
        data = json.load(f)
    page_title =data["pages"][0]["title"]

    #run random walks as many times as needed to build a desireable path
    print("***** running random walks")
    mod_threshold = True
    while mod_threshold:
        plot_similarity(G)
        threshold = float(input("Enter a threshold to try: "))
        path = rwf.DiGraphRandomWalk(G=G,niters=NUM_ITERATIONS,
                depth=DEPTH, threshold=threshold, start_tag=page_title)
        print(path)
        answer = input("Would you like to try another threshold? [Y/N]")
        if(answer != "Y" or answer !="y"): mod_threshold = False

    #builds all the data and dumps into a json
    with open(doc_title, "r") as f:
        data = json.load(f)

    info = []
    info.append(build_dict(0, data))
    info.append(build_dict(1, data))
    info.append(build_dict(2, data))
    info.append(build_dict(3, data))

    with open(page_title + "_web.json", "w") as f:
        json.dump(info,f,sort_keys=True, indent=4)
