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
# Tests whether or not the 
def test_all_stop_words():
    index_all_stops = Indexer("wikis/FirstTestXML.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    index_all_stops.ids_to_words_to_counts
    for word in testing_dict.keys():
        assert testing_dict[word][1] == 0.0

"""
------------------------------------
NO LINK FOR SOME PAGES TESTS
------------------------------------
"""
    
def test_indexer_no_links_for_some_pages():
    indexer = Indexer("wikis/testing/links_handling/SomeLinksEmpty.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: set(),
        3: {2, 4},
        4: set()
    }
    assert indexer.ids_to_links == expected_links

# Makes sure that PageRank handles the case where pages that link to nothing are considered to link to every page, except
# themselves.
def test_pagerank_weights_no_links_for_some_pages():
    indexer = Indexer("wikis/testing/links_handling/SomeLinksEmpty.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.3208, 0.0375, 0.3208, 0.3208], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.3208, 0.3208, 0.3208, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001) 

def test_pagerank_scores_no_links_for_some_pages():
    Indexer("wikis/testing/links_handling/SomeLinksEmpty.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3633, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2273, 0.001)

"""
---------------------------
IGNORE LINKS TO SELF TESTS
---------------------------
"""
def test_indexer_ignore_links_self():
    indexer = Indexer("wikis/testing/links_handling/LinksToSelf.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: {3},
        3: {2, 4},
        4: {2, 3}
    }
    assert indexer.ids_to_links == expected_links

def test_pagerank_weights_ignore_links_self():
    indexer = Indexer("wikis/testing/links_handling/LinksToSelf.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.0375, 0.0375, 0.8875, 0.0375], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.0375, 0.4625, 0.4625, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)

def test_pagerank_scores_ignore_links_self():
    Indexer("wikis/testing/links_handling/LinksToSelf.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3357, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4136, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2131, 0.001)              

"""
--------------------------
IGNORES LINK DUPLICATES
--------------------------
"""
def test_indexer_ignore_links_duplicates():
    indexer = Indexer("wikis/testing/links_handling/LinkDuplicates.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: {3},
        3: {2, 4},
        4: {2, 3}
    }
    assert indexer.ids_to_links == expected_links

def test_pagerank_weights_ignore_duplicates():
    indexer = Indexer("wikis/testing/links_handling/LinkDuplicates.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.0375, 0.0375, 0.8875, 0.0375], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.0375, 0.4625, 0.4625, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)

def test_pagerank_scores_ignore_duplicates():
    Indexer("wikis/testing/links_handling/LinkDuplicates.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3357, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4136, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2131, 0.001)

"""
------------------------
IGNORES EXTERNAL LINKS
------------------------
"""
def test_indexer_ignore_external_links():
    indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: {3},
        3: {2, 4},
        4: {2, 3}
    }
    assert indexer.ids_to_links == expected_links

def test_pagerank_weights_ignore_external_links():
    indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.0375, 0.0375, 0.8875, 0.0375], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.0375, 0.4625, 0.4625, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)

def test_pagerank_scores_ignore_external_links():
    Indexer("wikis/testing/links_handling/ExternalLinks.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3357, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4136, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2131, 0.001)

"""
---------------------------
IGNORING LEADS TO EMPTY
---------------------------
"""
def test_indexer_ignore_then_empty():
    indexer = Indexer("wikis/testing/links_handling/IgnoreThenEmpty.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: set(),
        3: {2, 4},
        4: set()
    }
    assert indexer.ids_to_links == expected_links

# Makes sure that PageRank handles the case where pages that link to nothing are considered to link to every page, except
# themselves.
def test_pagerank_weights_ignore_then_empty():
    indexer = Indexer("wikis/testing/links_handling/IgnoreThenEmpty.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.3208, 0.0375, 0.3208, 0.3208], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.3208, 0.3208, 0.3208, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001) 

def test_pagerank_scores_ignore_then_empty():
    Indexer("wikis/testing/links_handling/IgnoreThenEmpty.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3633, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2273, 0.001)


"""
---------------------------
PIPES TESTS
---------------------------
"""

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


























def test_pagerank_weights_metapages():
    indexer = Indexer("wikis/testing/links_handling/MetaPagesTest.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.3208, 0.3208, 0.3208], [0.0375, 0.0375, 0.8875, 0.0375], \
        [0.3208, 0.3208, 0.0375, 0.3208], [0.3208, 0.3208, 0.3208, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001) 


# def test_indexer_ignore_external_links():
#     indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml", "title_file.txt", "docs_file.txt", "words_file.txt")

#     expected_links = {
#         1: set(),
#         2: {3},
#         3: set(),
#         4: set()
#     }

#     # Words in links that are ignored - makes sure that they are considered in the corpus of words.
#     words_in_links = ["Mathematics", "Physics", "Python", "Gauss", "Fermat", "Newton"]
#     expected_words = stem_words(remove_stop_words(words_in_links))

#     actual_words = {}
#     file_io.read_words_file("words_file.txt", actual_words)

#     assert indexer.ids_to_links == expected_links
#     for x in expected_words:
#         assert x in actual_words.keys()

# def test_pagerank_weights_ignore_external_links():
#     indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
#     expected_weights = [[0.0375, 0.3208, 0.3208, 0.3208], [0.0375, 0.0375, 0.8875, 0.0375], \
#         [0.3208, 0.3208, 0.0375, 0.3208], [0.3208, 0.3208, 0.3208, 0.0375]]
#     for i in range(1, 5):
#         for j in range(1, 5):
#             indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001) 






































def test_pagerank_scores_examples():

    # PageRankExample1.xml
    Indexer("wikis/testing/pagerank/PageRankExample1.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.4326, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.2340, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.3333, 0.001)

    # PageRankExample2.xml
    Indexer("wikis/testing/pagerank/PageRankExample2.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.2018, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.3740, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.3867, 0.001)

    # PageRankExample3.xml
    Indexer("wikis/testing/pagerank/PageRankExample3.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0524, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.0524, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4476, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.4476, 0.001)

    # PageRankExample4.xml
    Indexer("wikis/testing/pagerank/PageRankExample4.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4625, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.4625, 0.001)



    



    


    



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