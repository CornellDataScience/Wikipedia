from bs4 import BeautifulSoup
import requests
import sys
STEM = "https://en.wikipedia.org"

def get_pages(category):
    """
    This method returns a list of all page titles displayed in a "Category" page.
    """
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

def get_links(page):
    """
    This method returns a list of links, which includes links from two sources:
    the current page and links in the corresponding category pages.
    (The categories are found at the bottom of the current page. )
    """
    page1 = requests.get(page)
    try:
        soup = BeautifulSoup(page1.text, "html5lib")
        links=[page[page.find('org')+3:]]
        # Find links to other articles within the current page
        notes = soup.find('span', id='Notes')
        for t in notes.parent.previous_siblings:
            if t.name == 'p' or t.name == 'ul':
                for a in t.find_all('a'):
                    if a['href'][:6] == '/wiki/' and a['class'] != 'mw-redirect':
                        links.append(a['href'][6:])

        # Find links to category pages at the bottom of the current page
        category_links = []
        category = soup.find('div', id='mw-normal-catlinks')
        for cate in category.children:
            if cate.name == 'ul':
                for a in cate.find_all('a'):
                    if a['href'][:6] == "/wiki/":
                        category_links.append(STEM+a['href'])
        # Find links in the category page
        for category_page in category_links:
            links += get_pages(category_page)
        # remove duplicate links
        return list(set(links))
    except AttributeError:
        print("Failure in finding links")

# By far the fastest way to read wikipedia pages
def read_pages(links):
    file_name= "raw_data.txt"
    myFile = open(file_name, 'a')
    for page in links:
        print("reading page: " + page)
        page1 = requests.get(STEM + '/wiki/' + page)
        try:
            soup = BeautifulSoup(page1.text, "html5lib")
            text = soup.find_all('p')
            full_text = ""
            title = soup.find('h1').getText() + "\n"
            for t in text:
                if not t.find('img') and (t.name == 'p' or t.name == 'ul'):
                    full_text += str(t.getText().replace('\n', ''))
            myFile.write(title)
            myFile.write(full_text + "\n")
        except AttributeError:
            print("invalid page, skipping")

if __name__ == '__main__':
    root_page = str(sys.argv[1])
    links = get_links(root_page)
    print('Relevant pages are as follows: ')
    print(links)
    print('Reading related ' + str(len(links)) + ' articles...')
    read_pages(links)
    print('Successfully scraped all pages in the list!')
