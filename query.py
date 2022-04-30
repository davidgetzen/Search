import file_io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()


class Querier:
    def __init__(self, title_path, doc_path, word_path, is_pagerank=False):
        self.title_path = title_path
        self.doc_path = doc_path
        self.word_path = word_path

    def get_query_words(self, query_text):
        query_words = query_text.strip().lower().split(" ")
        stop_removed = self.remove_stop_words(query_words)
        stemmed = self.stem_words(stop_removed)
        return stemmed

    def remove_stop_words(self, words):
        return [word for word in words if word not in STOP_WORDS]

    def stem_words(self, words):
        return [the_stemmer.stem(word) for word in words]

    def score_docs(self, stemmed_words):
