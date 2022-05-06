"""
This is our text_cleaner module. It contains important methods to tokenize,
remove stop words, and stem words.

We decided to create this module because its functions are used in Indexer,
Querier, and the test file. We didn't want to copy the same functions over and
over again.
"""

import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

the_stemmer = PorterStemmer()
STOP_WORDS = stopwords.words("english")

"""
Identifies using the Regex expression the tokens in the input string,
and returns them.

Parameters:
text - a string to tokenize.

Returns:
text_tokens - a list of tokens in the string given.
"""

def tokenize_text(text):
    n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
    text_tokens = re.findall(n_regex, text)
    return text_tokens

"""
Removes stop words, using nltk, from a list of strings given to it.

Parameters:
word_list - a list of strings to remove stop words from.

Returns:
A copy of the inputted list, without the stop words.
"""  

def remove_stop_words_and_lower(word_list):
    return [word.lower() for word in word_list if word.lower() not in STOP_WORDS]

"""
Stems and lower words, using the nltk PorterStemmer.

Parameters:
word_list - a list of words to stem and lower.

Returns:
A copy of the list, with words lowered and stemmed.
"""

def stem_words(word_list):
    return [the_stemmer.stem(word.lower()) for word in word_list]    