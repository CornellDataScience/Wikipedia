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
def read_desc(page, name):
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
        file_name=name + ".txt"
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
    full_text = ""
    links=[]
    title=""
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find_all('p')
        #extract text only before the "see also" section
        see_also = soup.find('span', id='See_also')
        title = str("\n" + soup.find('h1').getText() + "\n")
        for p in see_also.parent.previous_siblings:
            alt = p.find('img')
            if not alt and p.name == 'p':
                full_text += str(p.getText())#.encode('utf-8', 'ignore'))
                for a in p.find_all('a'):
                    if a['href'][:6] == "/wiki/": links.append(a['href'])
    except AttributeError:
        print("invalid page, skipping")
    filter(visible,full_text)
    file_name="linalg_text2.txt"
    print(title + full_text)
    myFile = open(file_name, 'a')
    myFile.write(title)
    myFile.write(full_text)
    return links

#read every link in the topic content
def read_links(page, name):
    #if depth == -1: return
    print("reading page: " + page)
    page1 = requests.get(page)
    file_name= name+".csv"
    links=[]
    title=""
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find_all('p')
        #extract text only before the "see also" section
        see_also = soup.find('span', id='See_also')
        title = str(soup.find('h1').getText().encode('utf-8'))
        with open('linagl_links2.csv', 'a', newline='') as csvfile:
            fieldnames = ['origin_link', 'outgoing_link','origin_title','outgoing_title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()
            for p in see_also.parent.previous_siblings:
                if p.name =='p':
                    for a in p.find_all('a'):
                        if a['href'][:6] == "/wiki/":
                            links.append(a['href'])
                            writer.writerow({'origin_link' : page.encode('utf-8'),
                            'outgoing_link': a['href'].encode('utf-8'),
                            'origin_title':title,
                            'outgoing_title':a['title'].encode('utf-8')})
    except AttributeError:
        print("invalid page, skipping")
    #file_name="linalg_text3.txt"
    return links
    #myFile = open(file_name, 'a')
    #print(title + "\n" + full_text)
    #return full_text
    #file_name = "page" + str(depth)  + str(i)+".csv

#return title + "\n" + full_text
if __name__ == '__main__':
    #links = read_links("https://en.wikipedia.org/wiki/Linear_algebra")
    #make_network("https://en.wikipedia.org/wiki/Linear_algebra", 2)
    #confirming that links written correctly
    """fieldnames = ['origin_link', 'outgoing_link','origin_title','outgoing_title']
    with open('linagl_links2.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()"""
    links = read_links("https://en.wikipedia.org/wiki/Linear_algebra", "linagl_links2")
    links_2 = []
    for i in links:
        links_2 = read_links(STEM+i,"linagl_links2")
        #for j in links_2:
            #read_(STEM+j)
    """with open('page.csv', 'w', newline='') as csvfile:
        fieldnames = ['origin_link', 'outgoing_link']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)    #for i in links:
        for row in reader:
            print(row['origin_link'] +" " + row['outgoing_link'])"""
