import re
import xml.etree.ElementTree as et
import file_io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()


class Indexer:
    def __init__(self, data_path, title_path):
        self.file_path = data_path
        self.title_path = title_path

    def parse_xml(self):
        root = et.parse(self.file_path).getroot()
        all_pages = root.findall("page")
        ids_to_titles = {}

        ids_to_words = {}

        for page in all_pages:

            page_id = int(page.find("id").text)  # int(page.find("id"))
            page_title = page.find("title").text.strip()
            ids_to_titles[page_id] = page_title

            page_text = page.find("text").text.lower()
            ids_to_words[page_id] = self.get_page_words(page_text)

        corpus = self.get_corpus(ids_to_words)
        words_to_ids_to_counts = {}

        # for doc_id in ids_to_words.keys(): # For each document id in ids_to_words
        #     for word in ids_to_words[doc_id]: # For each word in corpus of the document

        #         # If the word is not in the word -> id -> count, initialize a dict for it
        #         # with a count of 1.
        #         if word not in words_to_ids_to_counts.keys():
        #             words_to_ids_to_counts[word] = {doc_id: 1}
        #         # If it is there, check whether there is a count for the specific doc_id we're looping through.
        #         else:
        #             # If it is the case, add 1 to that count.
        #             if doc_id in words_to_ids_to_counts[word].keys():
        #                 words_to_ids_to_counts[word][doc_id] += 1
        #             # If not, initialize the count to 1.
        #             else:
        #                 words_to_ids_to_counts[word][doc_id] = 1

        for word in corpus:
            for id in ids_to_words.keys():
                if word not in words_to_ids_to_counts:
                    words_to_ids_to_counts[word] = {}
                words_to_ids_to_counts[word][id] = ids_to_words[id].count(word)

        file_io.write_title_file(self.title_path, ids_to_titles)

    def tokenize_text(self, text):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        text_tokens = re.findall(n_regex, text)
        return text_tokens

    def remove_stop_words(self, words):
        return [word for word in words if word not in STOP_WORDS]

    def stem_words(self, words):
        return [the_stemmer.stem(word) for word in words]

    def get_page_words(self, page_text):
        page_tokens = self.tokenize_text(page_text)
        page_without_stop_words = self.remove_stop_words(page_tokens)
        page_with_stemmed_words = self.stem_words(page_without_stop_words)
        return page_with_stemmed_words

    def get_corpus(self, ids_dict):
        corpus = []
        for words in ids_dict.values():
            for word in words:
                if word not in corpus:
                    corpus.append(word)
        return corpus
