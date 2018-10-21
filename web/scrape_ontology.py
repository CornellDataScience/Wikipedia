import json
from bs4 import BeautifulSoup as bs4
import requests
import csv
import re
import sys
import io
MAX_DEPTH = 3
STEM = "https://en.wikipedia.org"

def find(root_page):
    page = requests.get(root_page)
    parent_links = []
    try:
        soup = bs4(page.text, "html5lib")
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

def scrape_articles(lst):
    pass

if __name__ == '__main__':
    root_page = str(sys.argv[1])
    print(find(root_page))
