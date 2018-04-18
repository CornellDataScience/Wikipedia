from flask import Flask
from flask import request
from flask import render_template
import networkx as nx
import pandas as pd
import scraper
import similarity
import randomwalk
import show


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text1 = request.form['keyword']
    text2 = request.form['depth']

    root_page = text1
    depth = int(text2)

    if depth == 1: scraper.desc_1(root_page)
    elif depth == 2: scraper.desc_2(root_page)
    #plagiarismPercent = stringComparison.extremelySimplePlagiarismChecker(text1,text2)
    docs = similarity.compute_similarity(text1 + '_1.json')

    G = nx.Graph()
    G.add_edges_from(docs)
    G = G.to_directed()

    path = randomwalk.DiGraphRandomWalk(G, 7, 10, .2, text1.replace('_', ' '), True)
    print('The paths are: ')
    print(path)


    show.graph(path)
    return "<h1>Showing the result for  " + text1 + "</h1>"

if __name__ == '__main__':
    app.run()
