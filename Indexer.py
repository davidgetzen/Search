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

            page_id = int(page.find("id").text) # int(page.find("id"))
            page_title = page.find("title").text.strip()
            ids_to_titles[page_id] = page_title

            page_text = page.find("text").text.lower()
            ids_to_words[page_id] = self.get_page_words(page_text)

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