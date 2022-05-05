import pytest
from index import Indexer
from query import Querier
import file_io
import text_cleaner

"""
------- Indexer Text Parsing Tests ----------
"""

# Tests the case where one page has no text.
# Does so with the assertion that this page, identified by its ID,
# will not be included in the words_to_ids_to_relevance dict.

def test_indexer_page_no_text():
    Indexer("wikis/testing/text_parsing/EmptyPageTest.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    for word in testing_dict:
        assert 1 not in testing_dict[word].keys()


# Test on a collection of pages for which none have any text.
# Makes an assertion that the size of the words_to_ids_to_relevances
# dict written into words_file.txt will be empty.
def test_indexer_all_pages_empty():
    Indexer("wikis/testing/text_parsing/AllEmptyPagesTest.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
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
    Indexer("wikis/testing/text_parsing/UpperLowerTest.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    print(testing_dict)
    assert len(list(testing_dict.keys())) == 1

def test_indexer_lower_upper_multiple_pages():
    Indexer("wikis/testing/text_parsing/UpperLowerTestPlural.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    testing_dict = {}

    file_io.read_words_file("words_file.txt", testing_dict)
    assert len(testing_dict.keys()) == 1
    assert len(testing_dict["test"].keys()) == 3

# Tests the indexer on the text of a page consisting of all stop words.
# Asserts that none of the stop words will be included in the
# words_to_ids_to_relevance dict written into words_file.txt.

def test_indexer_all_stop_words():
    index_all_stops = Indexer("wikis/testing/text_parsing/AllStopWords.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    stop_words = text_cleaner.stem_and_lower_words(["the", "a", "an", "in"])
    for word in stop_words:
        assert word not in list(testing_dict.keys())

# Tests that words in the pages' text are stemmed, and that their original form
# is not in the list of parsed words.
def test_indexer_words_stemmed():
    Indexer("wikis/testing/text_parsing/AreWordsStemmed.xml", "title_file.txt",
                              "docs_file.txt", "words_file.txt")        
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    original_words = ["Computer", "Science", "Cheese", "Charger",
    "Stupid", "Hello", "Awesome"]
    stemmed = text_cleaner.stem_and_lower_words(original_words)
    for word in stemmed:
        assert word in list(testing_dict.keys())
    for word in original_words:
        assert word not in list(testing_dict.keys())

# Tests that special characters disappear in the process of tokenizing.
def test_indexer_special_characters():
    Indexer("wikis/testing/text_parsing/TextSpecialCharacters.xml", "title_file.txt",
                              "docs_file.txt", "words_file.txt")        
    testing_dict = {}
    file_io.read_words_file("words_file.txt", testing_dict)
    original_words = ["Computer", "Science", "Cheese", "Charger",
    "Stupid", "Hello", "Awesome"]
    special_chars = ["$", "%", ";", ",", "#", "@"]
    special = text_cleaner.stem_and_lower_words(original_words)
    for word in special:
        assert word in list(testing_dict.keys())
    for chara in special_chars:
        assert chara not in list(testing_dict.keys())

"""
------- Indexer Title Parsing Tests ----------
"""

# Tests whether the titles from a simple XML file are parsed correctly.
def test_basic_titles_parsing():
    Indexer("wikis/testing/titles/BasicTitles.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    titles_dict = {}
    file_io.read_title_file("title_file.txt", titles_dict)

    assert titles_dict[211] == "A Wonderful Page"
    assert titles_dict[52] == "An Amazing Page"
    assert titles_dict[27] == "A Mesmerizing Page"

# Tests whether the titles are stripped when parsed.
def test_stripped_titles():
    Indexer("wikis/testing/titles/StrippedTitles.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    titles_dict = {}
    file_io.read_title_file("title_file.txt", titles_dict)

    assert titles_dict[211] == "A Wonderful Page"
    assert titles_dict[52] == "An Amazing Page"
    assert titles_dict[27] == "A Mesmerizing Page"

# Ensures that titles are not "cleaned" when parsed (i.e., no special characters
# are taken away).
def test_titles_no_cleaning():
    Indexer("wikis/testing/titles/SpecialTitles.xml", "title_file.txt",
                         "docs_file.txt", "words_file.txt")
    titles_dict = {}
    file_io.read_title_file("title_file.txt", titles_dict)

    assert titles_dict[211] == '''$%%-2222(  ) [[['''
    assert titles_dict[52] == '''%""'ldkççé__***$$$%%$'''
    assert titles_dict[27] == ''';;;;;23048(()["à"])'''


"""
------- Indexer Links Parsing Tests ----------
"""
##################################
#### Parsing Links with Pipes ####
##################################

# Tests whether the program takes the right element for words vs. links when splitting on pipes.    
def test_indexer_links_pipe():
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipes.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2},
        2: {1},
        3: {2},
        4: {3}
    }

    # These words were ONLY apparent to the right of the pipe.
    words_in_links = ["Calculus", "Socrates", "CS", "computations"]
    expected_without_stop_words = text_cleaner.remove_stop_words(words_in_links)
    expected_words = text_cleaner.stem_and_lower_words(expected_without_stop_words)

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words.keys()

# Makes sure that the program establishes links between pages correctly even if some pages
# show up as the text of different pages (for example, a link would lead to Mathematics but mention CS)
def test_indexer_links_pipe_confusing():
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipesConfusing.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")

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
    indexer = Indexer("wikis/testing/links_handling/LinksWithPipesSpecial.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2},
        2: {1},
        3: {2},
        4: {3}
    }

    # These words were ONLY apparent to the right of the pipe.
    words_in_links = ["Calculus", "Socrates", "CS"]
    special_characters_in_words = ["$", "/", " ", "", "%"]

    expected_without_stop_words = text_cleaner.remove_stop_words(words_in_links)
    expected_words = text_cleaner.stem_and_lower_words(expected_without_stop_words)

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words
    for y in special_characters_in_words:
        assert y not in actual_words

##################################
### Parsing Links to Metapages ###
##################################

# Tests that the program does consider links to metapages and adds the text related to them correctly.
def test_indexer_meta_links():
    indexer = Indexer("wikis/testing/links_handling/MetaPagesTest.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2, 4},
        2: {3, 4},
        3: set(),
        4: set()
    }

    words_in_links = ["Category", "Computer", "Science", "Mathematics"]
    expected_without_stop_words = text_cleaner.remove_stop_words(words_in_links)
    expected_words = text_cleaner.stem_and_lower_words(expected_without_stop_words)

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words.keys()

# Makes sure that references to links are stripped and words are correctly added to the corpus.
def test_indexer_meta_links_spaces():
    indexer = Indexer("wikis/testing/links_handling/MetaPagesSpace.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt") 

    expected_links = {
        1: {2, 4},
        2: {3, 4},
        3: set(),
        4: set()
    }

    words_in_links = ["Category", "Computer", "Science", "Mathematics"]
    expected_without_stop_words = text_cleaner.remove_stop_words(words_in_links)
    expected_words = text_cleaner.stem_and_lower_words(expected_without_stop_words)

    actual_words = {}
    file_io.read_words_file("words_file.txt", actual_words)

    assert indexer.ids_to_links == expected_links
    for x in expected_words:
        assert x in actual_words.keys()

#########################################
### Case Sensitivity in Parsing Links ###
#########################################
# Tests that the program does consider links to metapages and adds the text related to them correctly.
def test_indexer_case_sensitive_links():
    indexer = Indexer("wikis/testing/links_handling/CaseSensitivity.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")

    expected_links = {
        1: {2, 3, 4},
        2: {3},
        3: {4},
        4: {3}
    }

    assert indexer.ids_to_links == expected_links

"""
-------- Indexer Relevance Scores Tests ----------
"""
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

"""
------- General and Edge PageRank Tests ----------
"""

#############################################
### Testing General PageRankExample XMLs ###
#############################################

# Uses the four PageRankExample XMLs given and makes sure
# that computed PageRank scores are accurate.
def test_pagerank_scores_examples():

    # PageRankExample1.xml
    Indexer("wikis/testing/pagerank/PageRankExample1.xml", \
        "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.4326, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.2340, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.3333, 0.001)

    # PageRankExample2.xml
    Indexer("wikis/testing/pagerank/PageRankExample2.xml", \
        "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.2018, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.3740, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.3867, 0.001)

    # PageRankExample3.xml
    Indexer("wikis/testing/pagerank/PageRankExample3.xml", \
        "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0524, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.0524, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4476, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.4476, 0.001)

    # PageRankExample4.xml
    Indexer("wikis/testing/pagerank/PageRankExample4.xml", \
        "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4625, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.4625, 0.001)

# Makes sure that the sum of all PageRank scores is one, for SmallWiki.
def test_pagerank_small_wiki_adds_up_to_1():
    Indexer("wikis/SmallWiki.xml", "title_file.txt", "docs_file.txt", \
         "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)
    sum = 0
    for rank in pagerank_scores.values():
        sum += rank
    assert sum == pytest.approx(1)    

##############################################
### Special Case: Some pages have no links ###
##############################################
    
# Makes sure that the links between pages are established correctly when some pages do not link to anything.
def test_indexer_no_links_for_some_pages():
    indexer = Indexer("wikis/testing/links_handling/SomeLinksEmpty.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
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
    indexer = Indexer("wikis/testing/links_handling/SomeLinksEmpty.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.3208, 0.0375, 0.3208, 0.3208], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.3208, 0.3208, 0.3208, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == \
                pytest.approx(expected_weights[i-1][j-1], 0.001) 

# Makes sure that computed scores are accurate when some pages link to nothing.
def test_pagerank_scores_no_links_for_some_pages():
    Indexer("wikis/testing/links_handling/SomeLinksEmpty.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3633, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2273, 0.001)

##################################################
### Special Case: None of the pages have links ###
##################################################

# Tests that an empty set is given when none of the pages have links.
def test_indexer_no_link_for_all_pages():
    indexer = Indexer("wikis/testing/links_handling/NoLinkForAll.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: set(),
        2: set(),
        3: set(),
        4: set()
    }
    assert indexer.ids_to_links == expected_links

# Tests that the weights are computed correctly when none of the pages have links.
# (i.e., that the special case where a page with no links has to link to everything 
# except itself is handled.)
def test_pagerank_weights_no_link_for_all_pages():
    indexer = Indexer("wikis/testing/links_handling/NoLinkForAll.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.3208, 0.3208, 0.3208], [0.3208, 0.0375, 0.3208, 0.3208], \
        [0.3208, 0.3208, 0.0375, 0.3208], [0.3208, 0.3208, 0.3208, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)

# Tests that the final PageRank scores in this special case of none of the pages having
# links are accurate.
def test_pagerank_scores_no_link_for_all_pages():
    Indexer("wikis/testing/links_handling/NoLinkForAll.xml", \
        "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(1/4, 0.001)
    assert pagerank_scores[2] == pytest.approx(1/4, 0.001)
    assert pagerank_scores[3] == pytest.approx(1/4, 0.001)
    assert pagerank_scores[4] == pytest.approx(1/4, 0.001)

###################################################
### Special Case: Some pages link to themselves ###
###################################################

# Makes sure that the program does not consider links in cases where a page links to itself./
def test_indexer_ignore_links_self():
    indexer = Indexer("wikis/testing/links_handling/LinksToSelf.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: {3},
        3: {2, 4},
        4: {2, 3}
    }
    assert indexer.ids_to_links == expected_links

# Tests that the weights are computed correctly - i.e., that links to themselves are indeed ignored in the
# computation.
def test_pagerank_weights_ignore_links_self():
    indexer = Indexer("wikis/testing/links_handling/LinksToSelf.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.0375, 0.0375, 0.8875, 0.0375], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.0375, 0.4625, 0.4625, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)

# Tests that the final PageRank scores are accurate, when some pages link to themselves.
def test_pagerank_scores_ignore_links_self():
    Indexer("wikis/testing/links_handling/LinksToSelf.xml", \
        "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3357, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4136, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2131, 0.001)              

#####################################################################
### Special Case: some pages mention the same link multiple times ###
#####################################################################

# Makes sure that the program ignores duplicates, i.e., does not add a page twice
# when it is already in the set of links.
def test_indexer_ignore_links_duplicates():
    indexer = Indexer("wikis/testing/links_handling/LinkDuplicates.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: {3},
        3: {2, 4},
        4: {2, 3}
    }
    assert indexer.ids_to_links == expected_links

# Ensures that duplicates are ignored when computing PageRank weights.
def test_pagerank_weights_ignore_duplicates():
    indexer = Indexer("wikis/testing/links_handling/LinkDuplicates.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.0375, 0.0375, 0.8875, 0.0375], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.0375, 0.4625, 0.4625, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)

# Ensures that duplicates are ignored for the final computation of PageRank scores.
def test_pagerank_scores_ignore_duplicates():
    Indexer("wikis/testing/links_handling/LinkDuplicates.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3357, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4136, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2131, 0.001)

####################################################
### Special Case: Some pages have external links ###
####################################################

# Ensures that the program does ignore external links (i.e., links outside the wiki).
def test_indexer_ignore_external_links():
    indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: {3},
        3: {2, 4},
        4: {2, 3}
    }
    assert indexer.ids_to_links == expected_links

# Ensures that the program does ignore external links when computing PageRank weights.
def test_pagerank_weights_ignore_external_links():
    indexer = Indexer("wikis/testing/links_handling/ExternalLinks.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.0375, 0.0375, 0.8875, 0.0375], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.0375, 0.4625, 0.4625, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001)

# Ensures that the program does ignore external links when giving final PageRank scores.
def test_pagerank_scores_ignore_external_links():
    Indexer("wikis/testing/links_handling/ExternalLinks.xml", \
        "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.0375, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3357, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.4136, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2131, 0.001)

##################################################################################################
### Special Case: Ignoring duplicates/external links lead to some pages having no links at all ###
##################################################################################################

# Makes sure that the case where ignoring pages leads to some pages not linking to anything
# is handled correctly.
def test_indexer_ignore_then_empty():
    indexer = Indexer("wikis/testing/links_handling/IgnoreThenEmpty.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_links = {
        1: {2},
        2: set(),
        3: {2, 4},
        4: set()
    }
    assert indexer.ids_to_links == expected_links

# Makes sure that weights are computed correctly in the case where ignoring pages 
# leads to some pages not linking to anything.
def test_pagerank_weights_ignore_then_empty():
    indexer = Indexer("wikis/testing/links_handling/IgnoreThenEmpty.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    expected_weights = [[0.0375, 0.8875, 0.0375, 0.0375], [0.3208, 0.0375, 0.3208, 0.3208], \
        [0.0375, 0.4625, 0.0375, 0.4625], [0.3208, 0.3208, 0.3208, 0.0375]]
    for i in range(1, 5):
        for j in range(1, 5):
            assert indexer.get_pagerank_weight(i, j) == pytest.approx(expected_weights[i-1][j-1], 0.001) 

# Makes sure that PageRank scores are computed correctly in the case where ignoring pages 
# leads to some pages not linking to anything.
def test_pagerank_scores_ignore_then_empty():
    Indexer("wikis/testing/links_handling/IgnoreThenEmpty.xml", \
         "title_file.txt", "docs_file.txt", "words_file.txt")
    pagerank_scores = {}
    file_io.read_docs_file("docs_file.txt", pagerank_scores)

    assert pagerank_scores[1] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[2] == pytest.approx(0.3633, 0.001)
    assert pagerank_scores[3] == pytest.approx(0.2047, 0.001)
    assert pagerank_scores[4] == pytest.approx(0.2273, 0.001)

"""
------- Querier Unit Tests ----------
"""

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
        assert querier_with_pagerank.ids_to_scores[id] != \
            querier.ids_to_scores[id]
        if id != 6:
            assert querier_with_pagerank.ids_to_scores[id] < \
                querier_with_pagerank.ids_to_scores[6]


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