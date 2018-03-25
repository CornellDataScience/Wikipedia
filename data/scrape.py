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
        filter(visible, desc_text)
        file_name="beyonce_desc.txt"
        myFile = open(file_name, 'a')
        myFile.write(title)
        myFile.write(desc_text + "\n")
        print(desc_text)
    except AttributeError:
        print("invalid file, skipping")
    return links

#Read all the text on the page and return a list of links on that pageS
def read_page(page):
    #if depth == -1: return
    print("reading page: " + page)
    page1 = requests.get(page)
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find_all('p')
        full_text = ""
        links=[]
        title = soup.find('h1').getText() + "\n"
        for t in text:
            alt = t.find('img')
            if not alt:
                full_text += str(t.getText().encode('utf-8', 'ignore'))
        text = soup.find("div",{"class": "mw-parser-output"})
        for a in text.find_all(href=True):
            if a['href'][:6] == "/wiki/": links.append(a['href'])
    except AttributeError:
        print("invalid page, skipping")
    filter(full_text, visible)
    file_name="linalg.txt"
    myFile = open(file_name, 'a')
    myFile.write(title)
    myFile.write(full_text)
    return links

#read every link in the topic content
def read_links(page):
    #if depth == -1: return
    print("reading page: " + page)
    page1 = requests.get(page)
    file_name="page.csv"
    #myFile = open(file_name, 'a')
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find_all('p')
        full_text = ""
        links=[]
        title = soup.find('h1').getText() + "\n"
        #myFile.write(title)
        text = soup.find("div",{"class": "mw-parser-output"})
        link = ""
        with open('page.csv', 'a', newline='') as csvfile:
            fieldnames = ['origin_link', 'outgoing_link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for a in text.find_all(href=True):
                link = a['href']
                if link[:6] == "/wiki/" and link[-3:] != "svg":
                    links.append(link)
                    #myFile.write(a['href'])
                    writer.writerow({'origin_link' : page.encode('utf-8'), 'outgoing_link': link.encode('utf-8')})
    except AttributeError:
        print("invalid page, skipping")
    return links
    #print(title + "\n" + full_text)
    #return full_text
    #file_name = "page" + str(depth)  + str(i)+".csv
    
def make_network(page, depth):
    if(page[-3:] != "svg"):
        if depth == 0:
            print("base case")
            read_page(page)
        else:
            print("running read on " + page)
            links = read_page(page)
            for i in links:
                print("branching from " + i)
                make_network(STEM + i, depth-1)

#return title + "\n" + full_text
if __name__ == '__main__':
    #links = read_links("https://en.wikipedia.org/wiki/Linear_algebra")
    #make_network("https://en.wikipedia.org/wiki/Linear_algebra", 2)
    #confirming that links written correctly
    links = read_desc("https://en.wikipedia.org/wiki/Linear_algebra")
    links_2 = []
    for i in links:
        links_2 = read_desc(STEM+i)
        for j in links_2:
            read_desc(STEM+j)
    """with open('page.csv', 'r', newline='') as csvfile:
        fieldnames = ['origin_link', 'outgoing_link']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)    #for i in links:
        for row in reader:
            print(row['origin_link'] +" " + row['outgoing_link'])"""

    #    links_2.append(read_page(STEM + i))
    #print(links_2)
    #read_desc()
