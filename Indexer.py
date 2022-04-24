import re
import xml.etree.ElementTree as et
import file_io
from nltk.corpus import stopwords

STOP_WORDS = stopwords.words('english')

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
            page_tokens = self.tokenize_text(page_text)
            page_without_stop_words = self.remove_stop_words(page_tokens)

            ids_to_words[page_id] = page_tokens

        file_io.write_title_file(self.title_path, ids_to_titles)
    
    def tokenize_text(self, text):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        text_tokens = re.findall(n_regex, text)
        return text_tokens

    def remove_stop_words(self, words):
        no_stop_words = []
        for word in words:
            if word not in STOP_WORDS:
                no_stop_words.append(word)
        return no_stop_words        
                
        





        