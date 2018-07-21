import re, os, pickle
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer


def get_stopwords():
    file_path = os.getcwd()+'/data/stopwords.txt'
    with open(file_path, 'r') as file:
        stopwords = file.read().split('\n')
        
    return stopwords


def normalize(texts, stopwords):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    tokenized = []
    for text in texts:
        text_normalized = []
        for word in text.split():
            word = word.lower()
            word = re.match('[a-z]+', word)
            if word is not None:
                word = stemmer.stem(word.group(0))
                if word not in stopwords:
                    text_normalized.append(stemmer.stem(word))
        tokenized.append(text_normalized)
    
    return tokenized


def get_vocabs():
    file_path = os.getcwd()+'/data/vocabs.pkl'

    with open(file_path, 'rb') as file:
        vocabs = pickle.load(file)

    return vocabs


def vectorize(tokenized, vocabs):
    vectorizer = CountVectorizer(vocabulary=vocabs)
    X = vectorizer.fit_transform([' '.join(text) for text in tokenized])
    
    return X