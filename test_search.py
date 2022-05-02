import pytest
from index import Indexer
import query
import file_io
import repl

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()



def test_indexer_page_no_text(): 
    index_empty_page = Indexer("wikis/EmptyPageTest.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    # assert [word for word in testing_dict.keys() == 0]
    # words_to_ids_to_relevance
    testing_dict.items()
    #assert [score for score in testing_dict.items()[2] == 0]
    # Return later
def test_lower_upper():
    index_upper_lower = Indexer("wikis/UpperLowerTest.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    assert testing_dict["tomato"][0] == 1.0
    # Test whether or not the count is the same for the same word upper-case 
    # and lower-case. Tests the values of words_to_ids_to_relevance on an XML 
    # with a single page, wherein the only word is written five times with
    # verying arrangements of upper-and-lower-case letters. 
# REPL throw exceptions
# All stop words
# No stop words
def test_all_stop_words():
    index_all_stops = Indexer("wikis/FirstTestXML.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)

    
    
    

# Tests whether the program takes the right element for words vs. links when splitting on pipes.    
def test_indexer_links_pipe():
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipes.xml", "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2},
        2: {1},
        3: {2},
        4: {3}
    }

    # These words were ONLY apparent to the right of the pipe.
    words_in_links = ["Calculus", "Socrates", "CS", "computations"]
    expected_words = stem_words(remove_stop_words(words_in_links))

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words.keys()

# Makes sure that the program establishes links between pages correctly even if some pages
# show up as the text of different pages (for example, a link would lead to Mathematics but mention CS)
def test_indexer_links_pipe_confusing():
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipesConfusing.xml", "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2},
        2: {4},
        3: {1},
        4: {2}
    }

    assert indexer.ids_to_links == expected_links

# Tests that the program does consider links to metapages and adds the text related to them correctly.
def test_indexer_meta_links():
    indexer = Indexer("wikis/testing/links_handling/MetaPagesTest.xml", "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2, 4},
        2: {3, 4},
        3: set(),
        4: set()
    }

    words_in_links = ["Category", "Computer", "Science", "Mathematics"]
    expected_words = stem_words(remove_stop_words(words_in_links))

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words.keys()

def test_indexer_ignore_external_links():
    indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml", "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: set(),
        2: {3},
        3: set(),
        4: set()
    }

    # Words in links that are ignored - makes sure that they are considered in the corpus of words.
    words_in_links = ["Mathematics", "Physics", "Python", "Gauss", "Fermat", "Newton"]
    expected_words = stem_words(remove_stop_words(words_in_links))

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words.keys()


    



# Query not in any documents/Empty Query
# Same relevance scores
# Same pagerank&relevance scores
# Page linking to itself -> nothing -> all other pages
# Link with pipe
# Meta-Link recognition
# Page with two pages linking it vs. page with one page linking it -
# influence on rank of linked doc
# All pages link to themselves/nothing
# Page with no text
# Two pages with the same title?
# A wordlist of only stop words (return an empty list)
# A wordlist of no stop words (return identical list)
# If [[Link | Word]] and Word are in same text, make sure Word is counted twice
# Removing stop words from the textual representations of links


# test_query = query.Querier("title_file.txt",
#                            "words_file.txt", "docs_file.txt")
# test_query.start_querying("computer science")

def remove_stop_words(words):
    return [word for word in words if word not in STOP_WORDS]            

def stem_words(words):
    return [the_stemmer.stem(word).lower() for word in words]