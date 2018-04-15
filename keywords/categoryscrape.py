# Adapted from Linnea's scraper to scrape category pages

#coding=utf-8
from bs4 import BeautifulSoup as bs4
import requests
import csv
import re

MAX_DEPTH = 3
STEM = "https://en.wikipedia.org"
#filtering out only raw text from the html file
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

# Read only the description of the page and return the raw text as a string

def read_desc(page):
    page1 = requests.get(page)
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find("div",{"class": "mw-parser-output"})
        desc_text = ""
        links = []
        toc = text.find("div", {"class": "toc"})
        title = soup.find('h1').getText() + "\n"
        for p in toc.previous_siblings:
            if p.name == "p":
                desc_text += str(p.getText().encode('utf-8', 'ignore'))
                for a in p.find_all('a'):
                    if a['href'][:6] == "/wiki/": links.append(a['href'])
        filter(visible,desc_text)
        file_name="evals_text.txt"
        myFile = open(file_name, 'a')
        myFile.write(title)
        myFile.write(desc_text + "\n")
        print(desc_text)
    except AttributeError:
        print("invalid file, skipping")
    return links

def find_links(page):
    page1 = requests.get(page)
    soup = bs4(page1.text, "html5lib")
    text = soup.find("div",{"class": "mw-content-ltr"})
    links = []
    for a in text.find_all(href=True):
        if a['href'][:6] == "/wiki/": links.append(a['href'])
    return links

def find_cats(page):
    page1 = requests.get(page)
    soup = bs4(page1.text, "html5lib")
    text = soup.find("div",{"class": "mw-content-ltr"})
    links = []
    for a in text.find_all(href=True):
        if a['href'][:6] == "/wiki/": links.append(a['href'])
    return links

#return title + "\n" + full_text
if __name__ == '__main__':
    links_main = find_links("https://en.wikipedia.org/wiki/Category:Linear_algebra")
    print("looking in main category:")
    for k in links_main:
        read_desc(STEM+k)
    links_cat = find_cats("https://en.wikipedia.org/wiki/Category:Linear_algebra")
    for i in links_cat:
        links_2 = find_links(STEM+i)
        print("\nlooking in: " + i)
        for j in links_2:
            read_desc(STEM+j)
