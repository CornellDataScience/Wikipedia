import json
from bs4 import BeautifulSoup as bs4
import requests
import csv
import re
import sys
MAX_DEPTH = 3
STEM = "https://en.wikipedia.org"

#filtering out only raw text from the html file
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

#build the json entry for a singular page
def read_page(page):
    #if depth == -1: return
    print("reading page: " + page)
    page1 = requests.get(page)
    full_text = ""
    links=[]
    title=""
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find_all('p')
        #extract text only before the "see also" section
        see_also = soup.find('span', id='See_also')
        title = str(soup.find('h1').getText())
        for p in see_also.parent.previous_siblings:
            alt = p.find('img')
            if not alt and p.name == 'p':
                full_text += str(p.getText())#.encode('utf-8', 'ignore'))
                for a in p.find_all('a'):
                    if a['href'][:6] == "/wiki/": links.append(a['href'])
    except AttributeError:
        print("invalid page, skipping")
    except KeyError: 
        pass
    filter(visible,full_text)
    #print(title + full_text)
    page_dict = {'title': title, 'url': page, 'links': links, 'text': full_text}
    return page_dict

def desc_1(root_page):
    data = {}
    data['pages'] = [] #nested array so can append new pages as needed
    data['pages'].append(read_page(root_page))
    origin_links = data['pages'][0]['links']
    for l in origin_links:
        data['pages'].append(read_page(STEM + l))
    rt = data['pages'][0]['title']
    with open(rt + ".json", 'w') as f: 
        json.dump(data, f,sort_keys=True, indent=4)
    
if __name__ == '__main__':
    root_page = str(sys.argv[1])
    desc_1(root_page)