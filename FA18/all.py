import similarity_new as sn
import randomwalk as rw
import makeGraph as mg

if __name__ == '__main__':
    scraped_file = sys.argv[1]
    m, d = preprocess('../data/' + scraped_file)
    sim_matrix = create_similarity_matrix(m, d)
    
