from __future__ import print_function
import sys
import pandas as pd
import nltk
import re
import io
from sklearn.cluster import KMeans
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stemmer = SnowballStemmer("english")
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def tdf(doc_name, num_clusters):
    docs = io.open(doc_name, mode="r", encoding="utf-8", errors="ignore").read()
    docs = re.sub(r"\[\d+\]", "", docs)
    docs = re.sub(r"b'", "", docs)
    docs = re.sub(r'\w*\d\w*', '', docs).split('\n')
    titles = [docs[i] for i in range(len(docs)) if i % 2 == 0]
    docs = [docs[i] for i in range(len(docs)) if i % 2 == 1] # Split titles and contents

    stopwords = nltk.corpus.stopwords.words('english')

    totalvocab_stemmed = []
    totalvocab_tokenized = []
    for i in docs:
        allwords_stemmed = tokenize_and_stem(i)
        totalvocab_stemmed.extend(allwords_stemmed)
        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)

    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)

    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.1, stop_words= stopwords, analyzer = 'word', 
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(docs) # Generating term-frequency-inverse-document-frequency matrix
    terms = tfidf_vectorizer.get_feature_names() # Get all the key features across documents
    km = KMeans(n_clusters=num_clusters, random_state = 1)
    km.fit(tfidf_matrix)
    clusters = km.labels_.tolist()
    results = { 'title': titles, 'docs': docs, 'cluster': clusters}

    frame = pd.DataFrame(results, index = [clusters] , columns = ['title', 'cluster'])
    print("Top terms per cluster:")
    print()
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')
        for ind in order_centroids[i, :6]:
            print(' %s' % vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0], end=',')
        print()
        print()
        print("Cluster %d titles:" % i, end='')
        for title in frame.loc[i]['title'].values.tolist():
            print(' %s,' % title, end='')
        print()
        print()
    
if __name__ == '__main__':
    a = str(sys.argv[1])
    b = int(sys.argv[2])
    tdf(a, b)
    

