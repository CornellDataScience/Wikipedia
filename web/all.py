import randomwalk as rw
import scrape_json as scrape

if __name__ == '__main__':
    root_page = str(sys.argv[2])
    depth = int(sys.argv[1])
    print(depth)
    print(root_page)
    if depth == 1: desc_1(root_page)
    elif depth == 2: desc_2(root_page)
