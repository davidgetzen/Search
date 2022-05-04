import file_io as io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import sys
import re

STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()


class Querier:
    def __init__(self, titles_dict, docs_dict, words_dict, is_pagerank=False):
        self.is_pagerank = is_pagerank
        self.titles_dict = titles_dict
        self.docs_dict = docs_dict
        self.words_dict = words_dict
        self.ids_to_scores = {}

    def start_querying(self, query_text):
        self.ids_to_scores = {}
        words = self.clean_words(query_text)
        self.score_docs(words)

        if len(self.ids_to_scores) == 0:
            print("Sorry! No search results were found.")
        else:
            self.get_final_results()

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
        sorted_docs = sorted(self.ids_to_scores.items(),
                             key=lambda x: x[1], reverse=True)
        i = 0
        while i < 10 and i < len(sorted_docs):
            doc_title = sorted_docs[i][0]
            print(str(i+1) + " - " + self.titles_dict[doc_title])
            i += 1

    def tokenize_query(self, query_text):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        text_tokens = re.findall(n_regex, query_text)
        return text_tokens

    def remove_stop_words(self, words):
        return [word for word in words if word not in STOP_WORDS]

    def stem_words(self, words):
        return [the_stemmer.stem(word) for word in words]

    def clean_words(self, query_text):
        tokens = self.tokenize_query(query_text.lower())
        stop_removed = self.remove_stop_words(tokens)
        stemmed = self.stem_words(stop_removed)
        return stemmed
 

def read_files(title_path, doc_path, word_path):

    titles_dict = {}
    docs_dict = {}
    words_dict = {}

    io.read_title_file(title_path, titles_dict)
    io.read_docs_file(doc_path, docs_dict)
    io.read_words_file(word_path, words_dict)

    return [titles_dict, docs_dict, words_dict]


if __name__ == "__main__":

    is_pagerank = sys.argv[1] == "--pagerank"

    if len(sys.argv) < 4 or (len(sys.argv) < 5 and is_pagerank):
        print("Too few arguments were given!")
        print("Usage is: query.py [--pagerank] <XML filepath> <title file> <docs file> <words file>")
        exit()
    elif not is_pagerank and "--" in sys.argv[1]:
        print(sys.argv[1] + " is not a valid flag!")
        exit()
    
    try:
        if is_pagerank:
            dicts = read_files(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            dicts = read_files(sys.argv[1], sys.argv[2], sys.argv[3])
    except FileNotFoundError as e:
        print("File " + e.filename + " was not found.")
        exit()
    except IndexError as e:
        print("The format of the titles file is incorrect!")
        exit()
    except ValueError as e:
        print("The format of the docs file or the words file is incorrect!")
        exit()

    querier = Querier(dicts[0], dicts[1], dicts[2], is_pagerank)

    while True:
        user_text = input(
            "Please enter your query (or type :quit to leave the program): ")
        if user_text == ":quit":
            break
        querier.start_querying(user_text)