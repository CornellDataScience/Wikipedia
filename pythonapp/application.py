from flask import request, render_template, redirect, url_for, Flask
import networkx as nx
import pandas as pd
import scraper
import similarity
import randomwalk
import show
import process_list
import json


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/result')
def do_result():
    data = request.args['data']
    # return render_template('result.html', image=image)
    return render_template('result.html', data=data)


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

    lst = process_list.process_list(path, 3)
    lst[0] = lst[0] + ['Placeholder']
    list.reverse(lst)
    result_json = process_list.generate_json(lst,0)
    print(result_json)
    with open('result.json', 'w') as fp:
        json.dump(result_json, fp, sort_keys = True, indent = 2)


    print('The paths are: ')
    print(path)


    show.graph(path)
    # return redirect(url_for('.do_result', image='..\/graph2.gv.png'))
    return redirect(url_for('.do_result', data=result_json))

    #return "<h1>Showing the result for  " + text1 + "</h1>"
    # return render_template('hello.html', name = user)

if __name__ == '__main__':
    app.run()
