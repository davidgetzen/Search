import file_io as io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import sys

STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()

class Querier:
    def __init__(self, title_path, doc_path, word_path, is_pagerank=False):
        self.is_pagerank = is_pagerank

        self.titles_dict = {}
        io.read_title_file(title_path, self.titles_dict) 

        self.words_dict = {}
        io.read_words_file(word_path, self.words_dict)

        self.docs_dict = {}
        io.read_docs_file(doc_path, self.docs_dict)

        self.ids_to_scores = {}

    def start_querying(self, query_text):
        words = self.get_query_words(query_text)
        self.score_docs(words)

        if len(self.ids_to_scores) == 0:
            print("Sorry! No search results were found.")
        else:
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
        for word in stemmed_words:
            if word in self.words_dict:
                for doc in self.words_dict[word]:
                    scalar = 1
                    if self.is_pagerank:
                        scalar = self.docs_dict[doc]
                    if doc not in self.ids_to_scores:
                        self.ids_to_scores[doc] = self.words_dict[word][doc] * scalar
                    else:
                        self.ids_to_scores[doc] += self.words_dict[word][doc] * scalar           

    def get_final_results(self):
        sorted_docs = sorted(self.ids_to_scores.items(), key=lambda x: x[1], reverse=True)

        i = 0
        while i <= 10 and i < len(sorted_docs):
            doc_title = sorted_docs[i][0]
            print(self.titles_dict[doc_title])
            i += 1

if __name__ == "__main__":
    while True:
        user_text = input("Please enter your query (or type :quit to leave the program): ")
        if user_text == ":quit":
            break

        if sys.argv[1] == "--pagerank":
            querier = Querier(sys.argv[2], sys.argv[3], sys.argv[4], True)
        else:
            querier = Querier(sys.argv[1], sys.argv[2], sys.argv[3])
        querier.start_querying(user_text)