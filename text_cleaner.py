import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

the_stemmer = PorterStemmer()
STOP_WORDS = stopwords.words("english")

def tokenize_text(text):
    n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
    text_tokens = re.findall(n_regex, text)
    return text_tokens

def remove_stop_words(word_list):
    return [word for word in word_list if word not in STOP_WORDS]               

def stem_and_lower_words(word_list):
    return [the_stemmer.stem(word.lower()) for word in word_list]    