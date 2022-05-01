from math import log, sqrt
import re
import xml.etree.ElementTree as et

import file_io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

STOP_WORDS = stopwords.words('english')
EPSILON = 0.15
DELTA = 0.001
the_stemmer = PorterStemmer()

class index:
    def __init__(self, data_path, title_path, words_path, docs_path):
        self.file_path = data_path
        self.title_path = title_path
        self.words_path = words_path
        self.docs_path = docs_path

        self.titles_to_ids = {}
        self.pagerank_weights = {}
        self.ids_to_links = {}
        self.ids_to_titles = {}

    def parse_xml(self):
        root = et.parse(self.file_path).getroot()
        all_pages = root.findall("page")

        ids_to_words_to_counts = {}
        words_to_ids_to_tfs = {}
        words_to_ids_to_relevance = {}

        for page in all_pages:

            page_id = int(page.find("id").text)  # int(page.find("id"))
            page_title = page.find("title").text.strip()
            self.ids_to_titles[page_id] = page_title
            self.titles_to_ids[page_title.lower()] = page_id

            # Add page_id to pagerank weights dictionary
            self.ids_to_links[page_id] = []

            page_text = page.find("text").text.strip().lower()
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

        self.filter_unvalid_links()
        ids_to_pageranks = self.compute_pagerank_scores()            

        file_io.write_title_file(self.title_path, self.ids_to_titles)
        file_io.write_words_file(self.words_path, words_to_ids_to_relevance)
        file_io.write_docs_file(self.docs_path, ids_to_pageranks)

    def tokenize_text(self, text):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        #n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+|""'''
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
        cleaned_list = []
        for i in range(len(words_list)):
            word = words_list[i]
            if self.is_link(word):
                word = word.strip("[]")
                link_to_add = ""
                if "|" in word:
                    splitted_word = word.split("|")
                    link_to_add = splitted_word[0]

                    words_in_link = splitted_word[1].split(" ")
                    cleaned_list.extend(words_in_link)
                else:
                    link_to_add = word
                    #words_list[i] = word
                    if ":" in word:
                        split_word = word.split(":")
                        cleaned_list.extend(split_word[0].split(" "))
                        cleaned_list.extend(split_word[1].split(" "))
                    else:
                        cleaned_list.extend(word.split(" "))
                self.add_pagerank_link(page_id, link_to_add)
            else:
                cleaned_list.append(word)
        return cleaned_list

    def is_link(self, input_str):
        return input_str[:2] == "[[" and input_str[len(input_str)-2:] == "]]"   

    def add_pagerank_link(self, current_id, linked_title):
        if self.ids_to_titles[current_id].lower() != linked_title.lower():
            self.ids_to_links[current_id].append(linked_title)

    def filter_unvalid_links(self):
        ids_to_links_ids = {}
        for doc_id, links in self.ids_to_links.items():
            ids_to_links_ids[doc_id] = set()
            for link in links:
                if link in self.ids_to_links[doc_id]:
                    if link in self.titles_to_ids.keys():
                        ids_to_links_ids[doc_id].add(self.titles_to_ids[link])
        self.ids_to_links = ids_to_links_ids


    def get_pagerank_weight(self, page_id, link_id):
        n = len(self.titles_to_ids)

        if link_id in self.ids_to_links[page_id]:
            n_k = len(self.ids_to_links[page_id])

            # Case where a page links to nothing.
            # We consider that it links to everything, except itself.
            if n_k == 0:
                n_k = n - 1

            return EPSILON/n + (1 - EPSILON)*(1/n_k)
        else:
            return EPSILON/n

    def compute_pagerank_scores(self):
        r_i = {}
        r_f = {}

        n = len(self.titles_to_ids)

        # Initializing values in r and r'
        for id in self.ids_to_links.keys():
            r_i[id] = 0
            r_f[id] = 1/n

        while self.euclidean_distance(r_i, r_f) > DELTA:
            r_i = r_f.copy()
            for page_j in self.ids_to_links.keys():
                r_f[page_j] = 0
                for page_i in self.ids_to_links.keys():
                    r_f[page_j] = r_f[page_j] + self.get_pagerank_weight(page_i, page_j) \
                         * r_i[page_i]

        return r_f                 

    def euclidean_distance(self, r_i, r_f):
        total_sum = 0
        for page_id in r_i.keys():
            total_sum += (r_f[page_id] - r_i[page_id])**2
        return sqrt(total_sum)