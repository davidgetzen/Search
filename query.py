import file_io as io
import text_cleaner
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import sys
import re

STOP_WORDS = stopwords.words('english')
the_stemmer = PorterStemmer()

"""
This is the Querier class.
It contains all the logic that handles the process of Querying documents.
"""


class Querier:

    """
    This is the constructor for Querier.
    It sets up the necessary data structures and initiates the Querying process.

    Parameters:
    - titles_dict: the ids_to_titles dictionary read in from title_path in the read_files function.
    - docs_dict: the ids_to_pageranks dictionary read in from docs_path in the read_files function.
    - words_dict: the words_to_ids_to_relevance dictionary read in from words_path in the read_files function.
    - is_pagerank: determines whether or not pagerank scores will be used in returning documents for a given query.

    Returns: 
    Nothing -- It starts the Querying process.
    """

    def __init__(self, titles_dict, docs_dict, words_dict, is_pagerank=False):
        self.is_pagerank = is_pagerank
        self.titles_dict = titles_dict
        self.docs_dict = docs_dict
        self.words_dict = words_dict
        self.ids_to_scores = {}
    """
    This is the start_querying function.
    It faciliatates the tokenization of the query text in addition to the 
    scoring of documents against the tokenized query. It then returns the 
    documents retrieved through the querying process. 

    Parameters:
    query_text - the text which documents will be scored-against and returned 
    
    Returns:
    Nothing. In the case where the query cannot be found in any of the 
    indexed documents, a print statement informing the user of this 
    situtation will be executed. In the case where the query is located 
    and documents are scored against it, scored documents will be 
    printed for the user. 

    """

    def start_querying(self, query_text):
        self.ids_to_scores = {}

        # Tokenizes, stems, and removes query words from
        # the query text. Also converts it to lower-case.
        words = self.get_query_words(query_text)
        self.score_docs(words)

        if len(self.ids_to_scores) == 0:
            print("Sorry! No search results were found.")
        else:
            self.get_final_results()
    """
    This is the score_docs function. In the case where the pagerank flag is
    set to True, it will populate the ids_to_scores dictionary with values 
    derived from the product of the relevance scores and the PageRank scores 
    of each document. 
    Parameters:
    stemmed_words - the stemmed, tokenized query text  
    
    Returns:
    Nothing. It populates the ids_to_scores dictionary. 

    """

    def score_docs(self, stemmed_words):
        for word in stemmed_words:
            if word in self.words_dict:
                for doc in self.words_dict[word]:
                    scalar = 1
                    # In the case where the --pagerank flag is True, 'scalar'
                    # will be updated from 1 to the PageRank value
                    # corresponding to the doc.
                    if self.is_pagerank:
                        scalar = self.docs_dict[doc]
                    if doc not in self.ids_to_scores:
                        self.ids_to_scores[doc] = self.words_dict[word][doc] * scalar
                    else:
                        self.ids_to_scores[doc] += self.words_dict[word][doc] * scalar
    """
    This is the get_final_results function. 
    This function sorts the key-value tuples of the ids_to_scores dictionary
    from greatest to least, then prints the titles corresponding to the ids
    for the user to see. 
    Parameters:
    None
    Returns:
    Nothing. It prints the top documents scored against the user's query. 

    """

    def get_final_results(self):
        # Converts each key-value pair in ids_to_scores to a list of
        # key-element tuples, then sorts it according to the
        # value of the score. Reverse is set to True so it's sorted
        # from the greatest value to the lowest value.
        sorted_docs = sorted(self.ids_to_scores.items(),
                             key=lambda x: x[1], reverse=True)
        i = 0
        while i < 10 and i < len(sorted_docs):
            doc_title = sorted_docs[i][0]
            print(str(i+1) + " - " + self.titles_dict[doc_title])
            i += 1

    """
    This is the get_query_words function. It will tokenize the query text,
    remove all stop words from it, stem it, and convert it to lower-case. 
    Parameters:
    query - the query text
    
    Returns:
    A list of each non-stop-word
    from the query text tokenized, stemmed, and in lower-case. 
    """

    def get_query_words(self, query_text):
        tokens = text_cleaner.tokenize_text(query_text)
        stop_removed = text_cleaner.remove_stop_words(tokens)
        stemmed = text_cleaner.stem_and_lower_words(stop_removed)
        return stemmed

    """
    This is the read_files function. It will read in data from the file paths
    taken as arguments. 
    Parameters:
    title_path - the path to the file containing the ids_to_titles dictionary
    doc_path - the path to the file containing the ids_to_pageranks dictionary
    word_path - the path to the file containing the words_to_ids_to_relevance
    dictionary. 
    
    Returns:
    A list of dictionaries, where titles_dict is populated with the information
    from ids_to_titles, docs_dict is populated with the information from 
    ids_to_pageranks, and words_dict is populated with the information from 
    words_to_ids_to_relevance. 
    """


def read_files(title_path, doc_path, word_path):

    titles_dict = {}
    docs_dict = {}
    words_dict = {}
    # Reads-in values from corresponding files, then populates dictionaries
    # accordingly.
    io.read_title_file(title_path, titles_dict)
    io.read_docs_file(doc_path, docs_dict)
    io.read_words_file(word_path, words_dict)

    return [titles_dict, docs_dict, words_dict]


"""
This is the main method. It is the one that allows code execution
when calling the query.py file. It handles cases where too many or too few
arguments are given, or when an invalid value is given for the 
--pagerank flag, by printing
informative messages.

Parameters:
None.

Returns:
None.

Throws: 
FileNotFoundError when the words file cannot be located.
IndexError when the titles file cannot be located.
ValueError when the docs file cannot be located. 
"""
if __name__ == "__main__":

    is_pagerank = sys.argv[1] == "--pagerank"

    if len(sys.argv) < 4 or (len(sys.argv) < 5 and is_pagerank):
        # Case where too few arguments are provided in the command line.
        print("Too few arguments were given!")
        print(
            "Usage is: query.py [--pagerank] <title file> <docs file> <words file>")
        exit()
    elif (len(sys.argv) > 4 and not is_pagerank) or len(sys.argv) > 5:
        # Case where too many arguments are provided in the command line.
        print("Too many arguments were given!")
        print(
            "Usage is: query.py [--pagerank] <title file> <docs file> <words file>")
        exit()
    elif not is_pagerank and "--" in sys.argv[1]:
        # Case where a value other than '--pagerank' is given as the
        # PageRank flag.
        print(sys.argv[1] + " is not a valid flag!")
        exit()

    try:
        if is_pagerank:
            dicts = read_files(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            dicts = read_files(sys.argv[1], sys.argv[2], sys.argv[3])
    except FileNotFoundError as e:
        # Case where format of words_file was invalid.
        print("File " + e.filename + " was not found.")
        exit()
    except IndexError as e:
        print("The format of the titles file is incorrect!")
        exit()
    except ValueError as e:
        print("The format of the docs file or the words file is incorrect!")
        exit()

    querier = Querier(dicts[0], dicts[1], dicts[2], is_pagerank)

    while True:
        user_text = input(
            "Please enter your query (or type :quit to leave the program): ")
        if user_text == ":quit":
            break
        querier.start_querying(user_text)