from math import log
from cv2 import split
import numpy
import re
import xml.etree.ElementTree as et

from sqlalchemy import true
import file_io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


STOP_WORDS = stopwords.words('english')
EPSILON = 0.15
the_stemmer = PorterStemmer()


class Indexer:
    def __init__(self, data_path, title_path, words_path):
        self.file_path = data_path
        self.title_path = title_path
        self.words_path = words_path
        self.titles_to_ids = {}
        self.pagerank_weights = {}
        self.ids_to_links = {}
        #self.pagerank_scores = {}
        # self.is_pagerank = is_pagerank (save for querying)
        # if self.is_pagerank == "true":
        #     self.is_pagerank = True
        # else:
        #     self.is_pagerank = False

    def parse_xml(self):
        root = et.parse(self.file_path).getroot()
        all_pages = root.findall("page")
        ids_to_titles = {}

        #ids_to_words = {}
        ids_to_words_to_counts = {}
        words_to_ids_to_tfs = {}
        words_to_idfs = {}
        words_to_ids_to_relevance = {}

        for page in all_pages:

            page_id = int(page.find("id").text)  # int(page.find("id"))
            page_title = page.find("title").text.strip()
            ids_to_titles[page_id] = page_title
            self.titles_to_ids[page_title] = page_id

            # Add page_id to pagerank weights dictionary
            self.ids_to_links[page_id] = []

            page_text = page.find("text").text.lower()
            page_words = self.get_page_words(page_text, page_id)

            # Populating ids_to_words_to_counts is done here.
            ids_to_words_to_counts[page_id] = {}
            for word in page_words:
                if word not in ids_to_words_to_counts[page_id]:
                    ids_to_words_to_counts[page_id][word] = 1
                else:
                    ids_to_words_to_counts[page_id][word] += 1

            # Term Frequencies Computations
            a_j = max(
                [pair for pair in ids_to_words_to_counts[page_id].items()], key=lambda x: x[1])[1]
            for word in ids_to_words_to_counts[page_id].keys():
                tf = (ids_to_words_to_counts[page_id][word])/a_j

                if word not in words_to_ids_to_tfs.keys():
                    words_to_ids_to_tfs[word] = {}
                words_to_ids_to_tfs[word][page_id] = tf

        # Computing Inverse Document Frequencies and Relevance
        n = len(ids_to_words_to_counts.keys())
        for word in words_to_ids_to_tfs.keys():
            n_i = len(words_to_ids_to_tfs[word].keys())

            idf = log(n/n_i)
            words_to_ids_to_relevance[word] = {}
            for id in words_to_ids_to_tfs[word]:
                words_to_ids_to_relevance[word][id] = idf * \
                    words_to_ids_to_tfs[word][id]

                # if page_id not in words_to_ids_to_tfs[word].keys():
                #     words_to_ids_to_tfs[word][page_id] = 1
                # else:
                #     words_to_ids_to_tfs[word][page_id] += 1

            # # Computing Term Frequencies
            # for id in ids_to_words_to_counts.keys():
            #  a_j = max(
            #      [pair for pair in ids_to_words_to_counts[id].items()], key=lambda x: x[1])[1]
            #  for word in ids_to_words_to_counts[id].keys():
            #      tf = (ids_to_words_to_counts[id][word])/a_j
            #      words_to_ids_to_tfs[word][id] = tf

            #ids_to_words[page_id] = self.get_page_words(page_text)

        # corpus = self.get_corpus(ids_to_words)
        # words_to_ids_to_counts = {}
        # ids_to_words_to_counts = {}
        # words_to_ids_to_tfs = {}
        # words_to_idfs = {}
        # words_to_ids_to_relevance = {}
        # # for doc_id in ids_to_words.keys(): # For each document id in ids_to_words
        # #     for word in ids_to_words[doc_id]: # For each word in corpus of the document

        # #         # If the word is not in the word -> id -> count, initialize a dict for it
        # #         # with a count of 1.
        # #         if word not in words_to_ids_to_counts.keys():
        # #             words_to_ids_to_counts[word] = {doc_id: 1}
        # #         # If it is there, check whether there is a count for the specific doc_id we're looping through.
        # #         else:
        # #             # If it is the case, add 1 to that count.
        # #             if doc_id in words_to_ids_to_counts[word].keys():
        # #                 words_to_ids_to_counts[word][doc_id] += 1
        # #             # If not, initialize the count to 1.
        # #             else:
        # #                 words_to_ids_to_counts[word][doc_id] = 1

        # for word in corpus:
        #     words_to_idfs[word] = 0.0
        #     for id in ids_to_words.keys():
        #         if word not in words_to_ids_to_counts:
        #             words_to_ids_to_counts[word] = {}
        #             words_to_ids_to_tfs[word] = {}
        #             words_to_ids_to_relevance[word] = {}
        #         words_to_ids_to_counts[word][id] = ids_to_words[id].count(word)
        #         words_to_ids_to_tfs[word][id] = 0.0
        #         words_to_ids_to_relevance[word][id] = 0.0

        # for id in ids_to_words.keys():
        #     ids_to_words_to_counts[id] = {}
        #     for word in ids_to_words[id]:
        #         if word not in ids_to_words_to_counts[id]:
        #             ids_to_words_to_counts[id][word] = ids_to_words[id].count(
        #                 word)

        # for id in ids_to_words_to_counts.keys():
        #     a_j = max(
        #         [pair for pair in ids_to_words_to_counts[id].items()], key=lambda x: x[1])[1]
        #     for word in ids_to_words_to_counts[id].keys():
        #         tf = (ids_to_words_to_counts[id][word])/a_j
        #         words_to_ids_to_tfs[word][id] = tf

        # for word in words_to_ids_to_counts.keys():
        #     n = len(words_to_ids_to_counts[word].keys())
        #     n_i = len([id for id in words_to_ids_to_counts[word]
        #               if words_to_ids_to_counts[word][id] != 0])
        #     words_to_idfs[word] = log(n/n_i)

        # for word in words_to_ids_to_tfs.keys():
        #     idf = words_to_idfs[word]
        #     for id in words_to_ids_to_tfs[word].keys():
        #         words_to_ids_to_relevance[word][id] = words_to_ids_to_tfs[word][id] * idf
        # think critically about how we populate the dictionary
        # if we don't encounter the word in a document, dont add it as an entry

        # page-ids to words to counts
        # page-id would only store words appearing on page
        # ids_to_words_to_counts
        file_io.write_title_file(self.title_path, ids_to_titles)
        file_io.write_words_file(self.words_path, words_to_ids_to_relevance)

    def tokenize_text(self, text):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        text_tokens = re.findall(n_regex, text)
        return text_tokens

    def remove_stop_words(self, words):
        return [word for word in words if word not in STOP_WORDS]

    def stem_words(self, words):
        return [the_stemmer.stem(word) for word in words]

    def get_page_words(self, page_text, page_id):
        page_tokens = self.tokenize_text(page_text)
        page_without_stop_words = self.remove_stop_words(page_tokens)
        page_with_stemmed_words = self.stem_words(page_without_stop_words)
        page_with_links_handled = self.handle_links(page_with_stemmed_words, page_id)
        return page_with_links_handled

    def handle_links(self, words_list, page_id):
        for i in range(len(words_list)):
            word = words_list[i]
            if word[:2] == "[[" and word[len(word)-2:] == "]]":
                word = word.strip("[]")
                if "|" in word:
                    splitted_word = word.split("|")
                    self.add_pagerank_link(page_id, splitted_word[0])
                    words_list[i] = splitted_word[1]
                else:
                    words_list[i] = word
        return words_list

    def get_corpus(self, ids_dict):
        corpus = []
        for words in ids_dict.values():
            for word in words:
                if word not in corpus:
                    corpus.append(word)
        return corpus

    def compute_word_relevances():
        pass
    # computing the ids to ids to weights dictionary
    # we'll use the titles to ids dictionary

    def add_pagerank_edge(self, current_id, linked_title):
        link_id = self.titles_to_ids[linked_title]
        self.ids_to_links[current_id].append(link_id)

    def get_pagerank_weight(self, page_id, link_id):
        n = len(self.titles_to_ids)
        if link_id in self.ids_to_links[page_id]:
            n_k = len(self.ids_to_links[page_id])
            return EPSILON/n + (1 - EPSILON)*(1/n_k)
        else:
            return EPSILON/n    

        #ids -> list of pages the page links to
        #we would get n_k with len of that list
        # we would re-compute n_k everytime
        
        # use this, but add a pagerank_weights dict with id -> weight.
        # it would give the weight for all pages page i links to.

