#coding=utf-8
from bs4 import BeautifulSoup as bs4
import requests
import csv

MAX_DEPTH = 3
STEM = "https://en.wikipedia.org"
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
    #print(title + "\n" + full_text)
    #return full_text
    #file_name = "page" + str(depth)  + str(i)+".csv"
    file_name="page.txt"
    myFile = open(file_name, 'a')
    myFile.write(title)
    myFile.write(full_text)
    return links
#return title + "\n" + full_text
if __name__ == '__main__':
    links = read_page("https://en.wikipedia.org/wiki/Topic_model")
    for i in links:
        read_page(STEM + i)
