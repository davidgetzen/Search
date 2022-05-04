import pytest
from index import Indexer
import file_io

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()

def test_basic_titles_parsing():
    Indexer("wikis/testing/titles/BasicTitles.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    titles_dict = {}
    file_io.read_title_file("title_file.txt", titles_dict)

    assert titles_dict[211] == "A Wonderful Page"
    assert titles_dict[52] == "An Amazing Page"
    assert titles_dict[27] == "A Mesmerizing Page"

def test_stripped_titles():
    Indexer("wikis/testing/titles/StrippedTitles.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    titles_dict = {}
    file_io.read_title_file("title_file.txt", titles_dict)

    assert titles_dict[211] == "A Wonderful Page"
    assert titles_dict[52] == "An Amazing Page"
    assert titles_dict[27] == "A Mesmerizing Page"

def test_titles_no_cleaning():
    Indexer("wikis/testing/titles/SpecialTitles.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    titles_dict = {}
    file_io.read_title_file("title_file.txt", titles_dict)

    assert titles_dict[211] == '''$%%-2222(  ) [[['''
    assert titles_dict[52] == '''%""'ldkççé__***$$$%%$'''
    assert titles_dict[27] == ''';;;;;23048(()["à"])'''


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
PARSING LINKS - PIPES
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

# We have encountered a very annoying bug when dealing with links that had weird characters after |
# (special characters, empty spaces...).
# This test is designed to make sure the program handles these cases correctly, by adding the correct words
# to the corpus of words and ignoring special characters.
def test_indexer_links_pipe_special_characters():
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipesSpecial.xml", "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2},
        2: {1},
        3: {2},
        4: {3}
    }

    # These words were ONLY apparent to the right of the pipe.
    words_in_links = ["Calculus", "Socrates", "CS"]
    special_characters_in_words = ["$", "/", " ", "", "%"]
    expected_words = stem_words(remove_stop_words(words_in_links))

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words
    for y in special_characters_in_words:
        assert y not in actual_words

"""
---------------------------
PARSING LINKS - META LINKS
---------------------------
"""

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

# Makes sure that references to links are stripped and words are correctly added to the corpus.
def test_indexer_meta_links_spaces():
    indexer = Indexer("wikis/testing/links_handling/MetaPagesSpace.xml", "title_file.txt", "docs_file.txt", "words_file.txt") 

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

# """
# ----------------------------------------------------------
# PARSING - DOES COUNT WORDS IN LINKS AS OTHER WORDS IN TEXT
# ----------------------------------------------------------
# """
# # Makes sure that one word is counted twice, even if one of the instances is in a link.
# # To do so, the program compares the relevance scores
# def test_indexer_multiple_counts_links():
#     Indexer("wikis/testing/links_handling/MultipleCountsLinks.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
#     word_relevances = {}
#     file_io.read_words_file("words_file.txt", word_relevances)

#     stemmed_math = stem_words(["mathematics"])[0]
#     print(word_relevances[stemmed_math])

#     #assert word_relevances[stemmed_math] > word_relevances[stemmed_math][2]

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

def test_pagerank_small_wiki_adds_up_to_1():
    Indexer("wikis/SmallWiki.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)
    sum = 0
    for rank in pagerank_scores.values():
        sum += rank
    assert sum == pytest.approx(1)
    
def remove_stop_words(words):
    return [word for word in words if word not in STOP_WORDS]            

def stem_words(words):
    return [the_stemmer.stem(word).lower() for word in words]

def test_hammad_weights():
    Indexer("wikis/HammadXML.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    indexer = Indexer("wikis/HammadXML.xml", "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.05, 0.475, 0.475], [0.475, 0.05, 0.475], \
        [0.9, 0.05, 0.05]]
    for i in range(1, 4):
        for j in range(1, 4):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)