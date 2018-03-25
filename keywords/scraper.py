#coding=utf-8
from bs4 import BeautifulSoup as bs4
import requests
import csv
import re
import sys

MAX_DEPTH = 3
STEM = "https://en.wikipedia.org"

#Read all the text on the page and return a list of links on that pageS
def read_page(page):
    #if depth == -1: return
    # print("reading page: " + page)
    page1 = requests.get(page)
    try:
        soup = bs4(page1.text, "html5lib")
        text = soup.find_all('p')
        full_text = ""
        # links=[]
        see_also = soup.find('span', id='See_also')
        title = soup.find('h1').getText()
        for p in see_also.parent.previous_siblings:
            if p.name == 'p':
                alt = p.find('img')
                if not alt:
                    full_text += str(p.getText().encode('utf-8', 'ignore'))
        
        # for t in text:
        #     alt = t.find('img')
        #     if not alt:
        #         full_text += str(t.getText().encode('utf-8', 'ignore'))
        
        # text = soup.find("div",{"class": "mw-parser-output"})
        # for a in text.find_all(href=True):
        #     if a['href'][:6] == "/wiki/": links.append(a['href'])
    

    except AttributeError:
        print("invalid page, skipping")
    # print("title", title)
    # print("full_text", full_text)
    return title, full_text
    # return links

#read every link in the topic content
def read_links(page):
    #if depth == -1: return
    # print("reading page: " + page)
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
        with open('page.txt', 'w') as txtfile:
            for a in text.find_all(href=True):
                link = a['href']
                if link[:6] == "/wiki/" and link[-3:] != "svg":
                    link = STEM + link
                    links.append(link)
                    print(link)
                    txtfile.write(link  + '\n')

        # with open('page.csv', 'a', newline='') as csvfile:
        #     fieldnames = ['origin_link', 'outgoing_link']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for a in text.find_all(href=True):
        #         link = a['href']
        #         if link[:6] == "/wiki/" and link[-3:] != "svg":
        #             links.append(link)
        #             #myFile.write(a['href'])
        #             writer.writerow({'origin_link' : page.encode('utf-8'), 'outgoing_link': link.encode('utf-8')})
    except AttributeError:
        print("invalid page, skipping")
    return links
    #print(title + "\n" + full_text)
    #return full_text
    #file_name = "page" + str(depth)  + str(i)+".csv"

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
    soup = bs4(page1.text, "html5lib")
    text = soup.find("div",{"class": "mw-parser-output"})
    desc_text = ""
    toc = text.find("div", {"class": "toc"})
    for p in toc.previous_siblings:
        if p.name == "p":
            desc_text += p.getText()
    filter(visible, desc_text)
    return desc_texts
#
# def make_network(page, depth):
#     if(page[-3:] != "svg"):
#         if depth == 0:
#             print("base case")
#             read_page(page)
#         else:
#             print("running read on " + page)
#             links = read_page(page)
#             for i in links:
#                 print("branching from " + i)
#                 make_network(STEM + i, depth-1)

#return title + "\n" + full_text
if __name__ == '__main__':
    #links = read_links("https://en.wikipedia.org/wiki/Linear_algebra")
    #make_network("https://en.wikipedia.org/wiki/Linear_algebra", 2)
    #confirming that links written correctly
    a = str(sys.argv[1])
    links = read_links("https://en.wikipedia.org/wiki/" + a)
    title, text = read_page("https://en.wikipedia.org/wiki/" + a)
    file_name= a + ".txt"
    myFile = open(file_name, 'w+')
    # myFile.write(title)
    # myFile.write(text)

    # subTopics = open("subtopics.txt", 'w+')
    for i in links:
        each_title, each_text = read_page(i)
        myFile.write(each_title + "\n")
        myFile.write(each_text + "\n")

    # links_2 = []
    # for i in links:
    #     links_2 = read_links(STEM+i)
    """with open('page.csv', 'r', newline='') as csvfile:
        fieldnames = ['origin_link', 'outgoing_link']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)    #for i in links:
        for row in reader:
            print(row['origin_link'] +" " + row['outgoing_link'])"""
    print("finished extracting the links")
    # links.append(read_page(STEM + i))
    #print(links_2)
    #read_desc()
