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
                    if a['href'][:6] == '/wiki/' and not a.has_attr("class"):
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
def read_pages(links, fileName):
    dic = {}
    # file_name= "raw_data_1130.txt"
    myFile = open(fileName, 'a')
    for page in links:
        print("reading page: " + page)
        page1 = requests.get(STEM + '/wiki/' + page)
        try:
            soup = BeautifulSoup(page1.text, "html5lib")
            # begin constructing dictionary
            notes = soup.find('span', id='Notes')
            for t in notes.parent.previous_siblings:
                if t.name == 'p' or t.name == 'ul':
                    for a in t.find_all('a'):
                        if a['href'][:6] == '/wiki/' and not a.has_attr("class"):
                            if a['href'][6:] in links:
                                if a['href'][6:] in dic:
                                    dic[a['href'][6:]] += 1
                                else:
                                    dic[a['href'][6:]] = 1
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
    return dic


if __name__ == '__main__':
    root_page = str(sys.argv[1])
    page_title = root_page.split("/")[-1]
    print("title",page_title)
    links = get_links(root_page)
    # print('Relevant pages are as follows: ')
    # print(links)
    # print('Reading related ' + str(len(links)) + ' articles...')
    titles_dict = read_pages(links, page_title)
    titles_dict = sorted(titles_dict.items(), key=lambda x: x[1], reverse=True)
    # print('Successfully scraped all pages in the list!')
    # print('\n')
    # print(titles_dict)
