"""This module calculates the cosine similarity between two documents in a
collection of documents and generates a cosine similarity matrix.

Then, it stores the results in two dictionaries in the following format:
dictionary (type-1): {document => a vector containing the similarity values between this ducument and each of the other documents}
dictionary2 (type-2): {(document1, document2) => similarity value}
"""


import numpy
import pandas as pd
import nltk
import re
import io
import sys
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

lst = []
def compute_similarity(docs):
    """
    A function to generate a dictionary of documents and their cosine similarity values with other documents.

    Precondition:
    docs: a .txt file with the title of a document on one line and the passage starts from the next line (in a single paragraph)
    type: an int with 1 representing the type-1 dictionary and 2 representing the type-2 dictionary
    """

    # docs = io.open(docs, mode="r", encoding="utf-8", errors="ignore").read()
    # docs = re.sub(r"\[\d+\]", "", docs)
    # docs = re.sub(r"b'", "", docs)
    # docs = re.sub(r"(\\\ W)", "", docs)
    # docs = re.sub(r'\w*\d\w*', '', docs).split('\n')
    file = json.load(open(docs))
    titles = []
    docs = []
    for i in range(len(file["pages"])):
        titles = titles + [file["pages"][i]["title"]]
    print("titles",titles)
    for i in range(len(file["pages"])):
        docs = docs + [file["pages"][i]["text"]]

    # dict["pages"][1]["title"]

    #
    # titles = [docs[i] for i in range(len(docs)) if i % 2 == 0]
    # docs = [docs[i] for i in range(len(docs)) if i % 2 == 1]

    # data preprocessing
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
                                    min_df=0.1, stop_words= stopwords,
                                    use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(docs)
    terms = tfidf_vectorizer.get_feature_names()
    cos_sim = cosine_similarity(tfidf_matrix)
    dict = {}
    terms_num = len(titles)

    lst = []
    for i in range(terms_num):
        for j in range(terms_num):

            # dict[(titles[i],titles[j])] = cos_sim[i][j]
            # lst = lst + [(titles[i],titles[j],{'similarity':cos_sim[i][j]})]
            lst = lst + [(titles[i],titles[j],cos_sim[i][j])]

    print('length before', len(lst))
    lst = list(set(lst))
    print('length after', len(lst))

    lst = list(map(lambda x: (x[0],x[1],{'similarity':x[2]}), lst))
    print("here is the list", lst)
    return lst

def tokenize_and_stem(text):
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("english")
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


if __name__ == '__main__':
    a = str(sys.argv[1])
    compute_similarity(a)
