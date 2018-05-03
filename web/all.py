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

def plot_similarity(G):
    weights = []
    for node1, node2 in G.edges():
        weights.append(G[node1][node2]['similarity'])
    # Display histogram of cosine similarity values
    n, bins, patches = plt.hist(weights, 10, facecolor='blue', alpha=0.5)
    plt.show()

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

if __name__ == '__main__':
    depth = int(sys.argv[1])
    root_page = str(sys.argv[2])
    print("depth: " + str(depth))
    print("root page: " +root_page)
    #get all the data
    """if depth == 1:
        t = scrape.desc_1(root_page)
    elif depth == 2:
        t = scrape.desc_2(root_page)
    print(t)"""
    doc_title = "../data/" + root_page[30:]+ "_"+str(depth)+".json"
    print("***** saved to file " + doc_title)

    #make the Graph
    print("***** finding similarity and pagerank")
    G = mg.make_prototype_graph(doc_title).to_directed()
    with open(doc_title, "r") as f:
        data = json.load(f)
    page_title =data["pages"][0]["title"]

    #run random walks
    print("***** running random walks")
    mod_threshold = True
    while mod_threshold:
        plot_similarity(G)
        threshold = float(input("Enter a threshold to try: "))
        path = rwf.DiGraphRandomWalk(G=G,niters=NUM_ITERATIONS,
                depth=DEPTH, threshold=threshold, start_tag=page_title)
        print(path)
        answer = input("Would you like to try another threshold? [Y/N]")
        if(answer != "Y"): mod_threshold = False

    with open(doc_title, "r") as f:
        data = json.load(f)

    info = []
    info.append(build_dict(0, data))
    info.append(build_dict(1, data))
    info.append(build_dict(2, data))
    info.append(build_dict(3, data))

    """info["topics1"] = []
    info["topics2"] = []
    info["topics3"] = []
    info["topics4"] = []

    info["topics1"] = (build_dict(0, data))
    info["topics2"] = (build_dict(1, data))
    info["topics3"] = (build_dict(2,data))
    info["topics4"] = (build_dict(3,data))"""

    with open(page_title + "_web.json", "w") as f:
        json.dump(info,f,sort_keys=True, indent=4)
