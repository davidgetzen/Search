import pytest
import index
import query
import file_io
import repl


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

test_index = index.Index("wikis/SmallWiki.xml", "title_file.txt",
                         "words_file.txt", "docs_file.txt")
test_index.parse_xml()
# test_query = query.Querier("title_file.txt",
#                            "words_file.txt", "docs_file.txt")
# test_query.start_querying("computer science")
