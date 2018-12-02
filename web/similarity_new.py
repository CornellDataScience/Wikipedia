import io
import re
import sys
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from gensim import corpora
from gensim.corpora import MmCorpus
from gensim import similarities
from gensim.models import TfidfModel, LsiModel


def clean(doc):
    # remove stopwords and words that are too short
    return [lemma.lemmatize(i, 'v') for i in word_tokenize(doc) if i not in stop and len(i) > 2]

def preprocess(file_name):
    docs = io.open(file_name, mode="r", encoding="utf-8", errors="ignore").read().split('\n') # list of strings
    titles = [docs[i] for i in range(len(docs)) if i % 2 == 0] # list of string titles
    contents = [docs[i] for i in range(len(docs)) if i % 2 == 1] # list of string contents
    contents = list(map(lambda x: re.sub(r"\d+","",x), contents)) # remove all digits from text

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


def create_similarity_matrix(doc_term_matrix, dictionary, fileName):
    model_tfidf = TfidfModel(doc_term_matrix, id2word=dictionary, normalize=False)
    MmCorpus.serialize('./corpus_tfidf.mm', model_tfidf[doc_term_matrix], progress_cnt=100)
    corpus_tfidf = MmCorpus('./corpus_tfidf.mm') # Loading back the corpus file after applying tf-idf
    model_lsi = LsiModel(corpus_tfidf, num_topics=15, id2word=dictionary)

    # Creating the similarity matrix with simple bag-of-words model
    # index = similarities.MatrixSimilarity(doc_term_matrix, num_features=len(dictionary))

    # Creating the similarity matrix with LSI model
    index = similarities.MatrixSimilarity(model_lsi[corpus_tfidf], num_features=len(dictionary)) # Applying LSI model to all vectors

    index.save('./similarity_matrix_' + fileName + '.mm')

    return index

if __name__ == '__main__':
    file = str(sys.argv[1])
    fileName = file.split('/')[-1]
    titleName = fileName[0:fileName.index('_raw_data.txt')]
    # name = file.split('/')[-1]
    print(titleName)
    m, d = preprocess(file)
    create_similarity_matrix(m, d, titleName)
