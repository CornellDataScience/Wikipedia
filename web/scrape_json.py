import json
from bs4 import BeautifulSoup as bs4
import requests
import csv
import re
import sys
import io
MAX_DEPTH = 3
STEM = "https://en.wikipedia.org"

#filters out the tag notation from any extracted text
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

#build the json entry for a singular page
def read_page(page):
    print("reading page: " + page)
    page1 = requests.get(page)
    full_text = ""
    links=[]
    desc_links = []
    desc_text = ""
    title=""
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find_all('p')
        #extract text only before the "see also" section
        see_also = soup.find('span', id='See_also')
        title = str(soup.find('h1').getText())
        toc = soup.find("div", {"class": "toc"})
        #will only take text from everything above the see also section
        for p in see_also.parent.previous_siblings:
            alt = p.find('img') #won't consider image alt text
            if not alt and p.name == 'p':
                full_text += str(p.getText())
                for a in p.find_all('a'):
                    if a['href'][:6] == "/wiki/": links.insert(0,a['href'])
        #for the sake of speed, will also only take links from the description
        for p in toc.previous_siblings:
            if p.name == "p":
                for a in p.find_all('a'):
                    if a['href'][:6] == "/wiki/": desc_links.insert(0,a['href'])
                desc_text = str(p.getText().encode('utf-8', 'ignore')) + desc_text
    #throws an AttributeError if the page isn't in the typical article format
    # ex. could be a page to a page describing a picture
    except AttributeError:
        print("invalid page, skipping")
    filter(visible,full_text)
    page_dict = {'title': title, 'url': page, 'links': links,
        'text': full_text, 'desc_links': desc_links, 'desc_text':desc_text}
    return page_dict

def desc_1(root_page):
    data = {}
    data['pages'] = [] #nested array so can append new pages as needed
    data['pages'].append(read_page(root_page))
    origin_links = data['pages'][0]['links']
    for l in origin_links:
        data['pages'].append(read_page(STEM + l))
    rt = data['pages'][0]['title']
    doc_title = "../data/" + root_page[30:]+ "_1.json"
    with io.open(doc_title, 'w', encoding="utf-8") as f:
        json.dump(data, f,sort_keys=True, indent=4)
    f.close()
    print(doc_title)
    return rt

#read descriptions at depth 2
#will only pull links from the intro paragraph to avoid pulling inordinate amounts of data
def desc_2(root_page):
    data = {}
    data['pages'] = [] #nested array so can append new pages as needed
    data['pages'].append(read_page(root_page))
    origin_links = data['pages'][0]['desc_links']
    for l in origin_links:
        data['pages'].append(read_page(STEM + l))
    data_2 = {}
    data_2['pages'] = []
    l = len(data['pages'])
    for i in range(1, l):
        p = data['pages'][i]
        for l in p['desc_links']:
            data['pages'].append(read_page(STEM + l))
    #data['pages'].append(data_2['pages'][:])"""
    rt = data['pages'][0]['title']
    doc_title = "../data/" + root_page[30:] + "_2.json"
    with io.open(doc_title, 'w', encoding="utf-8") as f:
        json.dump(data, f,sort_keys=True, indent=4)
        print("FNISHED SCRAPING")
        return rt

if __name__ == '__main__':
    root_page = str(sys.argv[2])
    depth = int(sys.argv[1])
    print(depth)
    print(root_page)
    if depth == 1: desc_1(root_page)
    elif depth == 2: desc_2(root_page)
