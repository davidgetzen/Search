from math import log, sqrt
import time
import xml.etree.ElementTree as et
import sys

import file_io
import text_cleaner

EPSILON = 0.15
DELTA = 0.001

"""
This is the Indexer class.
It contains all the logic that handles the process of Indexing documents.
"""

class Indexer:

    """
    This is the constructor for Indexer.
    It sets up the necessary data structures and initiates the Indexing process.

    Parameters:
    - data_path: the XML filepath.
    - title_path: the filepath of the file where the dictionary from doc. IDs to titles is written.
    - docs_path: the filepath of the file where the dictionary from doc. IDs to PageRank scores is written.
    - words_path: the filepath of the file where the dictionary from words to ids to relevances scores is written.

    Returns:
    Nothing -- It starts the Indexing process.
    """

    def __init__(self, data_path, title_path, docs_path, words_path):
        self.file_path = data_path
        self.title_path = title_path
        self.docs_path = docs_path
        self.words_path = words_path

        self.titles_to_ids = {}
        self.ids_to_links = {}
        self.ids_to_titles = {}

        self.start_time = time.time()

        print("Indexing... Please wait.")
        self.start_indexing()

    """
    This is the start_indexing() method.
    It contains the main loop that goes through all of the pages in the document,
    parses the text, computes scores, and writes files.
    It is certainly the function that contains the most logic.

    Parameters:
    None. It interacts with instance variables.
    
    Returns:
    Nothing. It writes the results of the computations in the files given to the Indexer.

    Throws:
    FileNotFoundError - if the XML file given is not found. This error is handled by the main method.
    """

    def start_indexing(self):
        
        # Parses the XML file given by the user.
        root = et.parse(self.file_path).getroot()
        all_pages = root.findall("page")

        # Sets up necessary local data structures to store results of various computations
        # on the dataset.
        ids_to_words_to_counts = {}
        words_to_ids_to_tfs = {}
        words_to_ids_to_relevance = {}
        ids_to_max_count = {}

        # Main Loop - Goes through each of the pages in the XML file.
        for page in all_pages:

            # Takes the ID of the page and its title, and adds them accordingly to
            # a ids_to_titles dictionary, and a titles_to_ids dictionary.
            page_id = int(page.find("id").text)
            page_title = page.find("title").text.strip()
            self.ids_to_titles[page_id] = page_title.strip()
            self.titles_to_ids[page_title.strip()] = page_id

            # Prepares the dictionary from page IDs to the pages they link to,
            # by initializing the value at key "page_id" to an empty list.
            self.ids_to_links[page_id] = []

            # Finds the text of the page, and calls the get_page_words method
            # which tokenizes and cleans the text, and handles links.
            page_text = page.find("text").text.strip()
            page_words = self.get_page_words(page_text, page_id)

            # Prepares the ids to words to counts dictionary by setting
            # the value at key "page_id" to an empty dictionary.
            ids_to_words_to_counts[page_id] = {}
            
            # Populates the ids_to_words to counts dictionary,
            # and keeps track of the max count for each page.
            max_count = 0
            for word in page_words:
                if word not in ids_to_words_to_counts[page_id]:
                    ids_to_words_to_counts[page_id][word] = 1
                else:
                    ids_to_words_to_counts[page_id][word] += 1
                if ids_to_words_to_counts[page_id][word] > max_count:
                    max_count = ids_to_words_to_counts[page_id][word]
    
            ids_to_max_count[page_id] = max_count

            # Populates the term frequency dictionary using the
            # dictionary at "page_id" in ids_to_words_to_counts.
            for word in ids_to_words_to_counts[page_id].keys():
                a_j = ids_to_max_count[page_id]
                tf = (ids_to_words_to_counts[page_id][word])/a_j

                if word not in words_to_ids_to_tfs.keys():
                    words_to_ids_to_tfs[word] = {}
                words_to_ids_to_tfs[word][page_id] = tf

        # Computes the Inverse Document Frequencies, and
        # populates the words_to_ids_to_relevance dictionary,
        # by multiplying stored term frequencies, and the computed
        # IDFs.
        n = len(ids_to_words_to_counts.keys())
        for word in words_to_ids_to_tfs.keys():
            n_i = len(words_to_ids_to_tfs[word].keys())
            idf = log(n/n_i)

            words_to_ids_to_relevance[word] = {}
            for id in words_to_ids_to_tfs[word]:
                words_to_ids_to_relevance[word][id] = idf * \
                    words_to_ids_to_tfs[word][id]

        # Calls a function to filter unvalid links, and compute final pagerank scores.
        self.filter_unvalid_links()
        ids_to_pageranks = self.compute_pagerank_scores()            

        # Writes each dictionary to the adequate files.
        file_io.write_title_file(self.title_path, self.ids_to_titles)
        file_io.write_words_file(self.words_path, words_to_ids_to_relevance)
        file_io.write_docs_file(self.docs_path, ids_to_pageranks)

        # Computes how long the process took and prints an informative message to the user.
        duration = round(time.time() - self.start_time, 2)
        print("Indexing is done! The process took " + str(duration) + " seconds.")
    
    """
    The get_page_words method handles text we give it by tokenizing it, cleaning it,
    and handling all links in it.

    Parameters:
    page_text - A generally large string containing the text of a page.
    page_id - The ID of the page whose text is given.

    Returns:
    final_word_list - A list of strings corresponding to all words in the page, including 
    the words inside links.
    """

    def get_page_words(self, page_text, page_id):
        page_tokens = text_cleaner.tokenize_text(page_text)
        page_with_links_handled = self.handle_links(page_tokens, page_id)
        page_without_stop_words = text_cleaner.remove_stop_words(page_with_links_handled)
        final_word_list = text_cleaner.stem_and_lower_words(page_without_stop_words)
        return final_word_list

    """
    Oh boy! This is the handle_links method. It takes in a list of strings,
    corresponding to the tokens of a page. It detects links present in the list,
    adds them to the list of links that each page links to, and makes sure
    that all words in links that should be considered are added to the corpus of each
    page.

    Parameters:
    words_list - A list of tokens in a page.
    page_id - The ID of the page whose tokens are given.

    Returns:
    cleaned_list - A list of strings corresponding to the previous page tokens,
    with all words that should be considered and were initially inside links.
    """

    def handle_links(self, words_list, page_id):
        # This list will ultimately hold all of the words in the corpus of the page,
        # including those initially imprisoned in [[]].
        cleaned_list = []

        for word in words_list:

            # Case 1: the word is a link.
            # Words in the link should be handled correctly, and the link
            # itself should be considered for PageRank.
            if self.is_link(word):
                word = word.strip("[]") # Removes the brackets.
                link_to_add = ""

                # Case 1a: There is a | inside the link.
                # The element to the left of the pipe is a link to a page, while
                # the element to the right is a set of words that should be added to the corpus.
                if "|" in word:
                    splitted_word = word.split("|")
                    link_to_add = splitted_word[0]
                    link_text = splitted_word[1]
                    cleaned_list.extend(text_cleaner.tokenize_text(link_text))

                # Case 1b: There is no | in the link.
                # The content of the link should be added to the corpus of words.
                else:
                    # The title of the link should be handled as is.
                    link_to_add = word

                    # Case 1bi. There is a ":" in the word. It is a metalink.
                    # We should make sure that all words are added properly
                    if ":" in word:
                        splitted_word = word.split(":")
                        link_text = splitted_word[0] + " " + splitted_word[1]
                        cleaned_list.extend(text_cleaner.tokenize_text(splitted_word[0]))
                        cleaned_list.extend(text_cleaner.tokenize_text(splitted_word[1]))

                    # Case 1bii. The link is just a normal link, with no ":" or "|"
                    # Its word are added to the corpus of words.
                    else:
                        cleaned_list.extend(text_cleaner.tokenize_text(word.strip()))

                # link_to_add is added to the pages page_id links to.
                self.add_pagerank_link(page_id, link_to_add.strip())

            # Case 2: the word is not a link.
            # It should be added as is in the cleaned_list. Nothing related to PageRank
            # should be handled.   
            else:
                cleaned_list.append(word)
        
        return cleaned_list # Final corpus is returned.


    """
    Checks whether a method is a link by checking the presence of brackets [[]]

    Parameters:
    input_str - A string.

    Returns:
    A boolean - True if input_str is a link, False if not.
    """

    def is_link(self, input_str):
        return input_str[:2] == "[[" and input_str[len(input_str)-2:] == "]]"

    """
    Adds the inputted title to the list of pages the page of id "current_id" links to,
    as long as it's not a link to itself.

    Parameters:
    current_id - the page ID for the page whose list of links we are trying to append to.
    linked_title - the title of the page we want "current_id" to link to.

    Returns:
    Nothing. Performs the operation by changing instance variables.
    """       

    def add_pagerank_link(self, current_id, linked_title):
        if self.ids_to_titles[current_id] != linked_title:
            self.ids_to_links[current_id].append(linked_title)


    """
    Filters all unvalid links in the initial ids_to_links dictionary.
    It removes duplicates, and links outside the corpus.
    When it's done, it replaces the existing self.ids_to_links dictionary
    with a dictionary from page_ids to sets of page IDs they link to.

    Parameters:
    None. The function interacts with instance variables.

    Returns:
    Nothing. It replaces the already existing dictionary.

    NB: The choice of "replacing" the existing dictionary might feel weird,
    but we have decided to do so for a question of efficiency. The older data
    that contains titles of links pages link to is now useless.
    """

    def filter_unvalid_links(self):
        ids_to_links_ids = {}
        for doc_id, links in self.ids_to_links.items():
            ids_to_links_ids[doc_id] = set()
            for link in links:
                if link in self.ids_to_links[doc_id]:
                    if link in self.titles_to_ids.keys():
                        ids_to_links_ids[doc_id].add(self.titles_to_ids[link])        
        self.ids_to_links = ids_to_links_ids

    """
    Gets the PageRank weight from a page to another.

    Parameters:
    page_id - the "starting" page.
    link_id - the "destination" page.

    Returns:
    A float, corresponding to the PageRank weights from page "page_id" 
    to page "link_id"
    """   

    def get_pagerank_weight(self, page_id, link_id):
        n = len(self.titles_to_ids)
        n_k = len(self.ids_to_links[page_id])

        # Case 1: The weight from a page to itself.
        if page_id == link_id:
            return EPSILON/n
        
        # Case 2: page_id does not link to link_id, and page_id links to other pages (n_k != 0)
        elif link_id not in self.ids_to_links[page_id] and n_k != 0:
            return EPSILON/n

        # Case 3: page_id does link to link_id, or page_id does not link to any pages.    
        else:

            # page_id does not link to any pages. By the PageRank algorithm,
            # we consider that it links to all of the pages, except itself.
            if n_k == 0:
                n_k = n - 1

            return (EPSILON/n) + (1 - EPSILON)*(1/n_k)

    """
    Computes PageRank scores, exactly as done in the PageRank pseudocode.

    Parameters:
    None. It interacts with instance variables.

    Returns:
    A dictionary from document IDs to PageRank scores, that will be later written
    in the docs_file.
    """   
    def compute_pagerank_scores(self):
        r_i = {}
        r_f = {}

        n = len(self.titles_to_ids)

        # Initializing values in r and r'
        for id in self.ids_to_links.keys():
            r_i[id] = 0
            r_f[id] = 1/n

        while self.euclidean_distance(r_i, r_f) > DELTA:
            r_i = r_f.copy()
            for page_j in self.ids_to_links.keys():
                r_f[page_j] = 0
                for page_i in self.ids_to_links.keys():
                    r_f[page_j] = r_f[page_j] + self.get_pagerank_weight(page_i, page_j) \
                         * r_i[page_i]

        return r_f.copy()

    """
    Computes the Euclidian distance between two dictionaries,
    which map document IDs to their respective PageRank weights.

    Parameters:
    r_i - Dictionary to compute distance from.
    r_f - Dictionary to compute distance to.

    Returns:
    A dictionary from document IDs to PageRank scores, that will be later written
    in the docs_file.
    """              
    def euclidean_distance(self, r_i, r_f):
        total_sum = 0
        for page_id in r_i.keys():
            total_sum += (r_f[page_id] - r_i[page_id])**2
        return sqrt(total_sum)

"""
This is the main method. It is the one that allows code execution
when calling the index.py file. It handles cases where too many arguments
are given, or when the XML file given is not found, by printing
informative messages.

Parameters:
None.

Returns:
None.
"""

if __name__ == "__main__":

    if len(sys.argv) > 5:
        print("Too many arguments were given!")
        print("Usage is: index.py <XML filepath> <title file> <docs file> <word file>")
    elif len(sys.argv) < 5:
        print("Too few arguments were given!")
        print("Usage is: index.py <XML filepath> <title file> <docs file> <word file>")
    else:
        try:
            Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        except FileNotFoundError as e: # Case where the XML file given is not found.
            print("File " + e.filename + " was not found!")