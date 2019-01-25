import json
from bs4 import BeautifulSoup
import requests
import csv
import re
import sys
import io
MAX_DEPTH = 3
import scrape_json
STEM = "https://en.wikipedia.org"

def find(root_page):
    page = requests.get(root_page)
    parent_links = []
    try:
        soup = BeautifulSoup(page.text, "html5lib")
        # text = soup.find_all('p')
        #extract text only before the "see also" section
        # see_also = soup.find('span', id='See_also')
        category = soup.find('div', id='mw-normal-catlinks')
        for cate in category.children:
            if cate.name == 'ul':
                for a in cate.find_all('a'):
                    if a['href'][:6] == "/wiki/": parent_links.append(STEM+a['href'])
    #throws an AttributeError if the page isn't in the typical article format
    # ex. could be a page to a page describing a picture
    except AttributeError:
        print("invalid page, skipping")
    # filter(visible,full_text)
    # page_dict = {'title': title, 'url': page, 'links': links,
    #     'text': full_text, 'desc_links': desc_links, 'desc_text':desc_text}
    return parent_links

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def get_pages(category):
    page = requests.get(category)
    soup = BeautifulSoup(page.content, 'html.parser')
    mw_category = soup.select('#mw-pages .mw-category-group a')
    acc = [i.get_text() for i in mw_category]
    key = soup.select('#mw-pages a[href*=Category:]') # key is a list of length 2
    while True:
        next_page = requests.get(STEM + key[-1]['href'])
        next_soup = BeautifulSoup(next_page.content, 'html.parser')
        next_mw_category = next_soup.select('#mw-pages .mw-category-group a')
        acc += [i.get_text() for i in next_mw_category]
        key = next_soup.select('#mw-pages a[href*=Category:]')
        if key[-1].get_text() == 'previous page': # no next pages any more
            break
    return acc

def scrape_articles(lst):
    pages_to_read = [get_pages(item) for item in lst] # 2D list

    for i in range(len(pages_to_read)):
        print('Reading page from Category ' + lst[i])
        for word in pages_to_read[i]:
            print(scrape_json.read_page('https://en.wikipedia.org/wiki/' + word))

if __name__ == '__main__':
    root_page = str(sys.argv[1])
    # print(get_pages(root_page))
    print(scrape_articles(find(root_page)))
