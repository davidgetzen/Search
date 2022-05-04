import pytest
from index import Indexer
from query import Querier
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
    assert len(list(testing_dict.keys())) == 1
    # Test whether or not the count is the same for the same word upper-case
    # and lower-case. Tests the values of words_to_ids_to_relevance on an XML
    # with a single page, wherein the only word is written five times with
    # verying arrangements of upper-and-lower-case letters.
# REPL throw exceptions
# All stop words
# No stop words
# Tests whether or not the


def test_indexer_all_stop_words():
    index_all_stops = Indexer("wikis/AllStopWords.xml", "title_file.txt",
                              "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    stop_words = ["the", "a", "an", "in"]
    for word in stop_words:
        assert word not in list(testing_dict.keys())


# Tests whether the program takes the right element for words vs. links when splitting on pipes.
def test_indexer_links_pipe():
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipes.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")

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
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipesConfusing.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2},
        2: {4},
        3: {1},
        4: {2}
    }

    assert indexer.ids_to_links == expected_links

# Tests that the program does consider links to metapages and adds the text related to them correctly.


def test_indexer_meta_links():
    indexer = Indexer("wikis/testing/links_handling/MetaPagesTest.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")

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
    indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: set(),
        2: {3},
        3: set(),
        4: set()
    }

    # Words in links that are ignored - makes sure that they are considered in the corpus of words.
    words_in_links = ["Mathematics", "Physics",
                      "Python", "Gauss", "Fermat", "Newton"]
    expected_words = stem_words(remove_stop_words(words_in_links))

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words.keys()

# Case to test later - query with all stop words?


def test_query_same_relevance_scores_all_docs():
    indexer = Indexer("wikis/testing/querying/SameRelevanceTest.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")
    querier = Querier("title_file.txt", "docs_file.txt", "words_file.txt")

    print(querier.start_querying("single"))
    for score in querier.ids_to_scores.values():
        assert score == 0.0
    theInit = 1
    for name in querier.ids_to_scores.keys():
        assert name == theInit
        theInit += 1


def test_query_same_pagerank_scores():
    indexer = Indexer("wikis/testing/querying/SameRelevanceTestSec.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")
    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)
    print(actual_words)
    querier = Querier("title_file.txt", "docs_file.txt", "words_file.txt")
    querier.is_pagerank = True
    querier.start_querying("second")

    # print(querier.titles_dict)

    #assert querier.start_querying("second")[0] == 'D'
    #assert querier.start_querying("second")[1] == 'E'
    print(querier.ids_to_scores)
    # assert querier.ids_to_scores[5] == querier.ids_to_scores[6]
    # assert querier.ids_to_scores[5] == max(
    #     list(querier.ids_to_scores.values()))
    # assert querier.ids_to_scores[6] == max(
    #     list(querier.ids_to_scores.values()))


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
