import file_io as io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from pprint import pprint

STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()


class Querier:
    def __init__(self, title_path, doc_path, word_path, is_pagerank=False):
        self.title_path = title_path
        self.doc_path = doc_path
        self.word_path = word_path
        self.is_pagerank = is_pagerank

        self.ids_to_scores = {}


    def start_querying(self, query_text):
        words = self.get_query_words(query_text)
        self.score_docs(words)
        self.get_final_results()



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
        words_dict = {}
        docs_dict = {}

        io.read_words_file(self.word_path, words_dict)
        io.read_docs_file(self.doc_path, docs_dict)

        for word in stemmed_words:
            if word in words_dict.keys():
                for doc in words_dict[word]:
                    if doc not in self.ids_to_scores.keys():
                        if self.is_pagerank:
                            self.ids_to_scores[doc] = words_dict[word][doc] \
                                * docs_dict[doc]
                        else:
                            self.ids_to_scores[doc] = words_dict[word][doc]
                    else:
                        if self.is_pagerank:
                            self.ids_to_scores[doc] += words_dict[word][doc] \
                                * docs_dict[doc]
                        else:
                            self.ids_to_scores[doc] += words_dict[word][doc]        

    def get_final_results(self):
        titles_dict = {}
        io.read_title_file(self.title_path, titles_dict)
        sorted_docs = sorted(self.ids_to_scores.items(), key=lambda x: x[1], reverse=True)
        for i in range(10):
            doc_title = sorted_docs[i][0]
            print(titles_dict[doc_title])

        #return sorted(self.ids_to_scores.items(), key=lambda x: x[1], reverse=True)

                                      