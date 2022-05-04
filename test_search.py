import pytest
from index import Indexer
from query import Querier
import file_io
import repl

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()

# Tests the case where one page has no text.
# Does so with the assertion that this page, identified by its ID,
# will not be included in the words_to_ids_to_relevance dict.


def test_indexer_page_no_text():
    index_empty_page = Indexer("wikis/EmptyPageTest.xml", "title_file.txt",
                               "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    for word in testing_dict:
        assert 1 not in testing_dict[word].keys()


# Test on a collection of pages for which none have any text.
# Makes an assertion that the size of the words_to_ids_to_relevances
# dict written into words_file.txt will be empty.
def test_indexer_all_pages_empty():
    index_empty_page = Indexer("wikis/testing/indexing/AllEmptyPagesTest.xml", "title_file.txt",
                               "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    assert len(testing_dict) == 0

# Tests whether or not the count is the same for the same word upper-case
# and lower-case. Tests the values of words_to_ids_to_relevance on an XML
# with a single page, wherein the only word is written five times with
# verying arrangements of upper-and-lower-case letters. Makes the
# assertion that the word will be identified as singular and
# written into the ids_to_words_to_relevance dict as one key.


def test_indexer_lower_upper():
    index_upper_lower = Indexer("wikis/UpperLowerTest.xml", "title_file.txt",
                                "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    # print(testing_dict[0])
    print(testing_dict)
    assert len(list(testing_dict.keys())) == 1


def test_indexer_lower_upper_multiple_pages():
    index_upper_lower = Indexer("wikis/UpperLowerTest.xml", "title_file.txt",
                                "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    assert len(list(testing_dict.keys())) == 1

# Tests the indexer on the text of a page consisting of all stop words.
# Asserts that none of the stop words will be included in the
# words_to_ids_to_relevance dict written into words_file.txt.


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


# A basic test of relevance score functionality.
# The first assertion block tests to make sure that
# only the keys of
# documents containing the word "minute" (tokenized as "minut")
# are in the returned words_dict_test dict.
# Additionally asserts that the maximum relevance value for
# the word "minute" (tokenized as "minut") is identified by the
# document in which it occurs the most.
def test_indexer_basic_relevance():
    indexer = Indexer("wikis/testing/indexing/BasicRelevanceTest.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")
    words_dict_test = {}
    file_io.read_words_file("words_file.txt", words_dict_test)

    assert 2 not in list(words_dict_test['minut'].keys())
    assert 3 not in list(words_dict_test['minut'].keys())
    assert 5 not in list(words_dict_test['minut'].keys())
    assert 1 in list(words_dict_test['minut'].keys())
    assert 4 in list(words_dict_test['minut'].keys())

    assert words_dict_test["minut"][1] == max(
        list(words_dict_test['minut'].values()))

# Test where the relevance scores returned for a word, "second", are
# all the same. As every document contains the word "second", the
# IDF value later implemented in the relevance calculation will be 0.0,
# allowing each document a relevance score of 0.0 for the word "second".


def test_indexer_relevance_all_same():
    indexer = Indexer("wikis/testing/indexing/BasicRelevanceTest.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")
    words_dict_test = {}
    file_io.read_words_file("words_file.txt", words_dict_test)

    for i in range(1, len(list(words_dict_test['second'].keys()))+1):
        assert i in list(words_dict_test['second'].keys())
    for val in list(words_dict_test['second'].values()):
        assert val == 0.0


def test_query_same_pagerank_scores():
    indexer = Indexer("wikis/testing/querying/SameRelevanceTestSec.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")
    words_dict_test = {}
    file_io.read_words_file("words_file.txt", words_dict_test)
    print(words_dict_test)
    titles_dict_test = {}
    file_io.read_title_file("title_file.txt", titles_dict_test)
    docs_dict_test = {}
    file_io.read_docs_file("docs_file.txt", docs_dict_test)

    querier = Querier(titles_dict_test, docs_dict_test, words_dict_test)
    querier.start_querying("second")

    querier_with_pg = Querier(
        titles_dict_test, docs_dict_test, words_dict_test)
    querier_with_pg.is_pagerank = True
    querier_with_pg.start_querying("second")

    assert words_dict_test["second"][4] == words_dict_test["second"][5]

    # print(querier.titles_dict)

    # assert querier.start_querying("second")[0] == 'D'
    # assert querier.start_querying("second")[1] == 'E'

    assert querier.ids_to_scores[4] == querier.ids_to_scores[5]
    assert querier.ids_to_scores[4] == max(
        list(querier.ids_to_scores.values()))
    assert querier.ids_to_scores[5] == max(
        list(querier.ids_to_scores.values()))
#     # Systems tests in google docs, record results with a screenshot

# Test where the first query is made with the word "single" without
# the PageRank flag set to "true." This returns an ids_to_scores
# dict where each id has the same score. A unit-test is made to ensure this.
# The second instance of Querier, querier_with_pagerank, is such that the
# PageRank flag is now set to "true". No document in the new ids_to_scores
# dict has the same value as the one before. Moreover, the document
# linked-to the most, F (id 6), is now returned as the id with the
# greatest score. A test is made to ensure that F has a greater score than
# any other id within the new ids_to_scores dict.


def test_query_score_docs():
    indexer = Indexer("wikis/testing/querying/DifferencePageRank.xml",
                      "title_file.txt", "docs_file.txt", "words_file.txt")

    words_dict_test = {}
    file_io.read_words_file("words_file.txt", words_dict_test)
    titles_dict_test = {}
    file_io.read_title_file("title_file.txt", titles_dict_test)
    docs_dict_test = {}
    file_io.read_docs_file("docs_file.txt", docs_dict_test)

    querier = Querier(titles_dict_test, docs_dict_test, words_dict_test)
    querier.start_querying("single")
    print("Without PageRank:", querier.ids_to_scores, '\n')

    querier_with_pagerank = Querier(
        titles_dict_test, docs_dict_test, words_dict_test)
    querier_with_pagerank.is_pagerank = True
    querier_with_pagerank.start_querying("single")
    print("With PageRank", querier_with_pagerank.ids_to_scores)

    for id in querier.ids_to_scores.keys():
        assert querier.ids_to_scores[id] == pytest.approx(
            0.22314355131420976, 0.001)

    assert querier_with_pagerank.ids_to_scores[6] == max(
        querier_with_pagerank.ids_to_scores.values())

    for id in querier_with_pagerank.ids_to_scores.keys():
        assert querier_with_pagerank.ids_to_scores[id] != querier.ids_to_scores[id]
        if id != 6:
            assert querier_with_pagerank.ids_to_scores[id] < querier_with_pagerank.ids_to_scores[6]


# def test_difference_page_rank_unit_test():

# def test_upper_lower_multiple_pages():

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
    # Querying: same relevance two docs, same relevance all docs, same pagerank/relevance two docs,

    # test_query = query.Querier("title_file.txt",
    #                            "words_file.txt", "docs_file.txt")
    # test_query.start_querying("computer science")


def remove_stop_words(words):
    return [word for word in words if word not in STOP_WORDS]


def stem_words(words):
    return [the_stemmer.stem(word).lower() for word in words]
