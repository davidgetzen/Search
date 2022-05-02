from math import log, sqrt
import re
import xml.etree.ElementTree as et
import sys

import file_io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

STOP_WORDS = stopwords.words('english')
EPSILON = 0.15
DELTA = 0.001
the_stemmer = PorterStemmer()

class Indexer:

    def __init__(self, data_path, title_path, docs_path, words_path):
        self.file_path = data_path
        self.title_path = title_path
        self.docs_path = docs_path
        self.words_path = words_path

        self.titles_to_ids = {}
        self.ids_to_links = {}
        self.ids_to_titles = {}

        self.parse_xml()

    def parse_xml(self):
        root = et.parse(self.file_path).getroot()
        all_pages = root.findall("page")

        ids_to_words_to_counts = {}
        words_to_ids_to_tfs = {}
        words_to_ids_to_relevance = {}
        ids_to_max_count = {}

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
            
            max_count = 0
            for word in page_words:
                if word not in ids_to_words_to_counts[page_id]:
                    ids_to_words_to_counts[page_id][word] = 1
                else:
                    ids_to_words_to_counts[page_id][word] += 1
                if ids_to_words_to_counts[page_id][word] > max_count:
                    max_count = ids_to_words_to_counts[page_id][word]
    
            ids_to_max_count[page_id] = max_count

            # Term Frequencies Computations
            #all_pairs = [pair for pair in ids_to_words_to_counts[page_id].items()]
            #if len(all_pairs) == 0:
            #    a_j = 
            #a_j = max(
                #[pair for pair in ids_to_words_to_counts[page_id].items()], key=lambda x: x[1])[1]
            for word in ids_to_words_to_counts[page_id].keys():
                a_j = ids_to_max_count[page_id]

                #if a_j == 0:
                    #continue
                
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
        text_tokens = re.findall(n_regex, text)
        #text_tokens = [token for token in re.findall(n_regex, text) if token not in ["", "\n", " ", "\0"]]
        return text_tokens

    def remove_stop_words(self, words):
        return [word for word in words if word not in STOP_WORDS]
        #new_list = []
        #for word in words:
            #if len(word) == 1:
                #new_list.append(word)
            #elif word not in STOP_WORDS:
                #new_list.append(word)
        #return new_list                    

    def stem_words(self, words):
        return [the_stemmer.stem(word) for word in words]
        # new_list = []
        # for word in words:
        #     if len(word) == 1:
        #         new_list.append(word)
        #     else:
        #         new_list.append(the_stemmer.stem(word))    
        # return new_list        


    def get_page_words(self, page_text, page_id):
        page_tokens = self.tokenize_text(page_text)
        page_with_links_handled = self.handle_links(page_tokens, page_id)
        page_without_stop_words = self.remove_stop_words(page_with_links_handled)
        page_with_stemmed_words = self.stem_words(page_without_stop_words)
        #page_with_stemmed_words = [word for word in self.stem_words(page_without_stop_words) if word != ""]
        #page_with_links_handled = self.handle_links(page_with_stemmed_words, page_id)
        return page_with_stemmed_words
        #return [word for word in page_with_links_handled if word != ""]

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
                    cleaned_list.extend(self.tokenize_text(splitted_word[1].strip()))
                else:
                    link_to_add = word
                    if ":" in word:
                        split_word = word.split(":")
                        cleaned_list.extend(self.tokenize_text(split_word[0].strip()))
                        cleaned_list.extend(self.tokenize_text(split_word[1].strip()))
                    else:
                        cleaned_list.extend(self.tokenize_text(word.strip()))
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
            #if len(ids_to_links_ids[doc_id]):
                #ids_to_links_ids.add(d)           
        self.ids_to_links = ids_to_links_ids


    def get_pagerank_weight(self, page_id, link_id):
        n = len(self.titles_to_ids)
        n_k = len(self.ids_to_links[page_id])

        if page_id == link_id:
            return EPSILON/n
        elif link_id not in self.ids_to_links[page_id] and n_k != 0:
            return EPSILON/n
        else:
            if n_k == 0:
                n_k = n - 1
            return (EPSILON/n) + (1 - EPSILON)*(1/n_k)

    def compute_pagerank_scores(self):
        r_i = {}
        r_f = {}

        n = len(self.titles_to_ids)
        #n = 2

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

        return r_f.copy()           

    def euclidean_distance(self, r_i, r_f):
        total_sum = 0
        for page_id in r_i.keys():
            total_sum += (r_f[page_id] - r_i[page_id])**2
        return sqrt(total_sum)

if __name__ == "__main__":
    Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])