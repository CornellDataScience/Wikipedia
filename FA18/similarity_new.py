import io
import re
import sys
from operator import itemgetter
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from gensim import corpora
from gensim.corpora import MmCorpus
from gensim import similarities
from gensim.models import TfidfModel, LsiModel
from gensim.models.ldamodel import LdaModel as Lda


def clean(doc):
    # remove stopwords and words that are too short
    stop = set(stopwords.words('english')) # set of stopwords
    lemma = WordNetLemmatizer()
    return [lemma.lemmatize(i, 'v') for i in word_tokenize(doc) if i not in stop and len(i) > 2]

def read_data(file_name):
    docs = io.open(file_name, mode="r", encoding="utf-8", errors="ignore").read().split('\n') # list of strings
    titles_raw = [docs[i] for i in range(len(docs)) if i % 2 == 0] # list of string titles
    contents_raw = [docs[i] for i in range(len(docs)) if i % 2 == 1] # list of string contents
    titles = []
    contents = []
    for i in range(len(titles_raw)):
        if contents_raw[i] != '':
            titles.append(titles_raw[i])
            contents.append(contents_raw[i])
    titles = list(set(titles))
    contents = list(set(contents))
    return titles, contents


def preprocess(contents):
    stop = set(stopwords.words('english')) # set of stopwords
    lemma = WordNetLemmatizer()
    cleaned = [clean(page.lower()) for page in contents]

    dictionary = corpora.Dictionary(cleaned)
    dictionary.filter_extremes(no_below=3, no_above=0.7)
    stoplist = set('also use make people know many call include part find become like mean often different usually take wikt come give well get since type list say change see refer actually iii aisne kinds pas ask would way something need things want every str'.split())
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    dictionary.filter_tokens(stop_ids)
    dictionary.filter_n_most_frequent(50)

    # Creating document-term matrix from vocabulary (dictionary)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in cleaned]

    return doc_term_matrix, dictionary


def cluster(doc_term_matrix, num, word_dict):
    ldamodel = Lda(doc_term_matrix, num_topics=num, id2word = word_dict)
    doc_topics = ldamodel.get_document_topics(doc_term_matrix, minimum_probability=0.20) # needs tuning
    result = [[] for i in range(num)]
    for k,topic in enumerate(doc_topics):
        # Some articles do not have a topic
        if topic:
            topic.sort(key = itemgetter(1), reverse=True)
            result[topic[0][0]].append(k)
    return [map(lambda x: titles[x], result[k]) for k in len(result)]

def create_mapping(titles):
    return {i:name for i,name in enumerate(titles)}


def create_similarity_matrix(doc_term_matrix, dictionary):
    model_tfidf = TfidfModel(doc_term_matrix, id2word=dictionary, normalize=False)
    MmCorpus.serialize('./corpus_tfidf.mm', model_tfidf[doc_term_matrix], progress_cnt=100)
    corpus_tfidf = MmCorpus('./corpus_tfidf.mm') # Loading back the corpus file after applying tf-idf
    model_lsi = LsiModel(corpus_tfidf, num_topics=15, id2word=dictionary)

    # Creating the similarity matrix with simple bag-of-words model
    # index = similarities.MatrixSimilarity(doc_term_matrix, num_features=len(dictionary))

    # Creating the similarity matrix with LSI model
    index = similarities.MatrixSimilarity(model_lsi[corpus_tfidf], num_features=len(dictionary)) # Applying LSI model to all vectors

    # index.save('./similarity_matrix_' + fileName + '.mm')

    return index





# if __name__ == '__main__':
#     file = str(sys.argv[1])
#     fileName = file.split('/')[-1]
#     titleName = fileName[0:fileName.index('_raw_data.txt')]
#     # name = file.split('/')[-1]
#     print(titleName)
#     t, c = read_data(file)
#     m, d = preprocess(c)
#     create_similarity_matrix(m, d)
