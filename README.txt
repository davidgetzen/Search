##############################################################
            GENERAL INFORMATION ABOUT THE PROJECT
##############################################################

*** Group Members ***
- Ayman Benjelloun Touimi
- David Getzen

*** Known Bugs ***
None :)

*** Instructions ***
Before querying, the user has to start the indexing process for their XML database.

To run the Indexer, the user should type the following command:
python index.py <XML filepath> <titles filepath> <docs filepath> <words filepath>

The titles file will contain all of the titles in the database, as well as their IDs.
The docs file will have pagerank scores for each document.
The words file will have the term relevance of each word, per document.

Then, the user can start the Querier, using the following command:
python query.py [--pagerank] <titles filepath> <docs filepath> <words filepath>

The user can specify the optional –pagerank flag if they wish to use the PageRank algorithm.

After that, a REPL will start allowing users to initiate as many queries as they wish, by typing terms and pressing Enter. The querier will then return the first ten results (or fewer, if less than ten are found).

The user can also quit the program by typing the special term “:quit”.

*** How the pieces of our program fit together ***

Before a user is able to make a query, a call to index.py within the command line 
is made. Within the main method of index.py, the number of arguments is verified 
as valid before any further steps are taken. If the number of arguments given is 
within the valid range, an instance of the Indexer class is created with each input 
in the command line taken as an argument. Within the Indexer class, data_path, 
docs_path, titles_path and words_path are initialized as instance variables, with 
data_path representing the location of the read-in XML document, docs_path representing 
the file that an ids_to_pageranks dictionary will get written into, titles_path representing 
the file that an ids_to_titles dictionary will get written into, and words_path representing 
the file that a words_to_ids_to_relevance dictionary will get written into. Next, 
three dictionaries, titles_to_ids, ids_to_links, and ids_to_titles, are initialized as 
additional instance variables. In the constructor, a call made to start_indexing() is 
then made; start_indexing() will iterate through the text of each page and make a call 
to the helper function get_page_words(page_text, page_id), where the first argument is
the text of a given document and the second is its ID. 

The function get_page_words(page_text, page_id) will facilitate the parsing of text and links, 
tokenization, stemming, and removal of stop words for every page. The function will defer 
tokenization to the use of the module text_cleaner, which contains the function 
tokenize_text(page_text). Moreover, get_page_words(page_text, page_id) will then also make a 
call to the helper function handle_links(page_tokens, page_id) on the tokenized text returned by 
text_cleaner.tokenize_text(page_text) to strip and tokenize the text of each link within a document.
The links the page refers to are then recorded in an ids_to_links dictionary populated by the helper 
method add_pagerank_link(current_id, linked_title). Within get_page_words(page_text, page_id), 
two more calls are made to the functions remove_stop_words(page_with_links_handed) and 
stem_and_lower_words(page_without_stop_words), the former of which removes all stop words 
from the tokenized, link-handled page, and the latter reduces each word to its lower-case stem. 

After the call to get_page_words(page_text, page_id) is completed, the term frequencies and 
inverse document frequencies are computed for each word, and the relevance scores are computed 
for each document. Before PageRank scores are calculated for each document, a call is made to 
the function filter_unvalid_links(), which serves to populate the ids_to_links_to_ids hashmap, 
recording the ids of the documents linked-to by the id of each page. Lastly, the ids_to_pageranks 
dictionary is populated with a call made to the compute.pagerank.scores() function, and the 
ids_to_titles, words_to_ids_to_relevance, and ids_to_pageranks dictionaries are respectively 
written to the files at title_path, words_path, and docs_path. 

After the call to index.py has completed, a call can then be made to query.py within the command line. 
If the first argument within the command line, the –pagerank flag, is set to “true”, then the 
PageRank calculations performed during indexing will be considered in scoring the returned 
documents for a given query. Otherwise, the documents will be returned in an order corresponding 
to their relevance scores alone. In either case, an instance of the Querier class will then 
be called after the arguments are given to the command line. This instance of the Querier class
will be called with elements of the dicts list returned by the read_files(title_path, doc_path, word_path)
function, which will return a list of the dictionaries read in from the files read out by Indexer. 

Next, a call is made to the function get_query_words(query_text), which will make a 
call of its own to the tokenize_text(query_text), remove_stop_words(tokens), and 
stem_and_lower_words(stop_removed) functions, performing tokenization, the removal of stop words, 
and the stemming and lowering of words within the query words. Next, a call will be made to the 
score_docs(stemmed_words) function, which will populate the ids_to_scores dictionary with scores 
for each document; if the is_PageRank flag is set to False, then these figures will be computed 
solely from the relevance scores of each document. Otherwise, they will be returned from the products 
of the relevance and PageRank scores for each document. Lastly, a call is made to get_final_results(), 
which will return the top 10 document results for the given query; in the case where less than 
10 document results exist, the amount of documents that do exist will be returned. 

For any additional details on our implementation, please consult the comments written in index.py and query.py.

*** Absent or Extra Features ***
As far as we know, we should’ve implemented all of the features required for full functionality. 
As for extra features, we simply added a stopwatch for the indexing process: when Indexing is done,
the program informs the user of how long it took to complete the Indexing process.

##############################################################
                        SYSTEM TESTS
##############################################################

***********************************
  CALLS TO index.py AND query.py
***********************************

*** index.py ***
TEST ONE: Passing in a XML file that doesn't exist.
Expected output: An informative message specifying that the XML file could not be found.

Input: python index.py "wikis/MedWiki1.xml" "titles.txt" "docs.txt" "words.txt"
Output: File wikis/MedWiki1.xml was not found!

TEST TWO: The XML file exists, but is not in the right format (i.e., another type of file is given)
Expected output: An informative message specifying that the XML file given is not in the right format.

(here, we give a python file instead of an XML)
Input: python index.py "query.py" "title_file.txt" "docs_file.txt" "words_file.txt"
Output: The format of the XML file given is not valid.

*** query.py ***
TEST ONE: Invalid flag that doesn’t correspond with pagerank.
Expected output: An informative message that the flag is incorrect.

Input: python query.py –-rankpage titles.txt docs.txt words.txt
Output: --rankpage is not a valid flag!

TEST TWO: Repeat terms for the word file and doc file arguments (i.e, wrong file is given for docs_file).
Expected output: An informative message telling us that one of the inputs (either the docs or the titles file) 
is not in the right format.

Input: python query.py --pagerank titles.txt words.txt words.txt
Output: The format of the docs file or the words file is incorrect!

TEST THREE: Give a wrong file in lieu of the title_file.
Expected output: An informative message telling us that the format of the title file is not recognized.

Input: python query.py –-pagerank words.txt docs.txt words.txt
Output: The format of the titles file is incorrect! 

TEST FOUR: Too few arguments are given (with --pagerank) 
Expected output: An informative message about the problem and an indication of how to properly use the program.

Input: python query.py –-pagerank titles.txt words.txt” 
Output: “Too few arguments were given! 
Usage is: query.py [--pagerank] <title file> <docs file> <words file>”

TEST FIVE: Too few arguments are given (without --pagerank) 
Expected output: An informative message about the problem and an indication of how to properly use the program.

Input: python query.py titles.txt words.txt” 
Output: “Too few arguments were given! 
Usage is: query.py [--pagerank] <title file> <docs file> <words file>”

TEST SIX: One of the file-path arguments is misspelled. 
Expected output: An informative message saying that the file wasn’t found.

Input: python query.py --pagerank titles.txt docs.txt werds.txt
Output: “File werds.txt was not found.” 

SEVENTH CASE: Too many arguments are given, (with -–pagerank).
Input: python query.py --pagerank titles.txt docs.txt words.txt anotherone.txt furthermore.txt
Expected output: An informative message about the problem and an indication of how to properly use the program.

Output: “Too many arguments were given!
Usage is: query.py [--pagerank] <title file> <docs file> <words file>”

SEVENTH CASE: Too many arguments are given, (without --pagerank).
(here, we want to make sure that the code knows that four arguments is too much when no –-pagerank flag is added).
Input: python query.py titles.txt docs.txt words.txt anotherone.txt 
Expected output: An informative message about the problem and an indication of how to properly use the program.

Output: “Too many arguments were given!
Usage is: query.py [--pagerank] <title file> <docs file> <words file>”

EIGTH CASE: The files given exist, but they are all empty.
Expected output: Nothing specific, just that none of the queries give results.

Input: python query.py "title_file.txt" "docs_file.txt" "words_file.txt"
Output: "Please enter your query (or type :quit to leave the program): hello
Sorry! No search results were found.
Please enter your query (or type :quit to leave the program): "

***********************************
  QUERY RESULTS FOR SPECIAL CASES
***********************************





***********************************
  OUR RESULTS FOR MEDWIKI QUERIES
***********************************
For all of the queries, we get a 10/10, with almost exactly the same order (when compared to TA results).

1a. "baseball" (without PageRank)
1 - Oakland Athletics
2 - Minor league baseball
3 - Miami Marlins
4 - Fantasy sport
5 - Kenesaw Mountain Landis
6 - Out
7 - October 30
8 - January 7
9 - Hub
10 - February 2

1b. "baseball" (with PageRank)
1 - Ohio
2 - February 2
3 - Oakland Athletics
4 - Kenesaw Mountain Landis
5 - Miami Marlins
6 - Netherlands
7 - Minor league baseball
8 - Kansas
9 - Fantasy sport
10 - Pennsylvania

2a. fire (without PageRank)
1 - Firewall (construction)
2 - Pale Fire
3 - Ride the Lightning
4 - G?tterd?mmerung
5 - FSB
6 - Keiretsu
7 - Hephaestus
8 - Izabella Scorupco
9 - KAB-500KR
10 - Justin Martyr

2b. fire (with PageRank)
1 - Falklands War
2 - Justin Martyr
3 - Firewall (construction)
4 - Empress Suiko
5 - New Amsterdam
6 - Pale Fire
7 - Montoneros
8 - Hermann G?ring
9 - Nazi Germany
10 - Navy

3a. "cats" (without PageRank)
1 - Kattegat
2 - Kiritimati
3 - Morphology (linguistics)
4 - Northern Mariana Islands
5 - Lynx
6 - Politics of Lithuania
7 - Freyja
8 - Isle of Man
9 - Nirvana (UK band)
10 - Autosomal dominant polycystic kidney

3b. "cats" (with PageRank)
1 - Netherlands
2 - Pakistan
3 - Morphology (linguistics)
4 - Northern Mariana Islands
5 - Kattegat
6 - Normandy
7 - Kiritimati
8 - Portugal
9 - Hong Kong
10 - Illinois

4a. "United States" (without PageRank)
1 - Federated States of Micronesia
2 - Imperial units
3 - Joule
4 - Knowledge Aided Retrieval in Activity Context
5 - Elbridge Gerry
6 - Martin Van Buren
7 - Pennsylvania
8 - Finite-state machine
9 - Louisiana
10 - Metastability

4b. "United States" (with PageRank)
1 - Netherlands
2 - Ohio
3 - Illinois
4 - Michigan
5 - Pakistan
6 - International Criminal Court
7 - Franklin D. Roosevelt
8 - Pennsylvania
9 - Norway
10 - Louisiana

5a. "united" (without PageRank)
1 - Imperial units
2 - Joule
3 - Gauss (unit)
4 - Knowledge Aided Retrieval in Activity Context
5 - Inch
6 - Imperialism in Asia
7 - Elbridge Gerry
8 - Martin Van Buren
9 - FSB
10 - Los Angeles International Airport

5b. "united" (with PageRank)
1 - Netherlands
2 - Pakistan
3 - Franklin D. Roosevelt
4 - Illinois
5 - Norway
6 - Ohio
7 - Portugal
8 - Korean People's Army
9 - Falklands War
10 - International Criminal Court

6a. "watch" (without PageRank)
1 - Shock site
2 - Martin Waldseem?ller
3 - G?tterd?mmerung
4 - Fahrenheit 451
5 - Kraftwerk
6 - Prometheus Award
7 - Mandy Patinkin
8 - Nirvana (UK band)
9 - Gregory Chaitin
10 - Luanda

6b. "watch" (with PageRank)
1 - International Criminal Court
2 - Luanda
3 - North Pole
4 - Joseph Stalin
5 - Fahrenheit 451
6 - Shock site
7 - Martin Waldseem?ller
8 - Franklin D. Roosevelt
9 - Norway
10 - Kraftwerk

7a. "pope" (without PageRank)
1 - Pope Alexander IV
2 - Pope Benedict III
3 - Pope Gregory V
4 - Pope Gregory VIII
5 - Pope Gregory XIV
6 - Pope Formosus
7 - Pope Eugene II
8 - Pope Clement III
9 - Pope Alexander VIII
10 - Pope

7b. "pope" (with PageRank)
1 - Pope
2 - Pope Urban VI
3 - Pope Paul VI
4 - Pope Gregory VIII
5 - Pope Clement III
6 - Pope Alexander IV
7 - Pope Benedict III
8 - Pope Gregory V
9 - Pope Gregory XIV
10 - Pope Formosus

8a. "battle" (without PageRank)
1 - Paolo Uccello
2 - J.E.B. Stuart
3 - Navy
4 - Heart of Oak
5 - Front line
6 - Irish mythology
7 - Oda Nobunaga
8 - Girolamo Aleandro
9 - Mehmed II
10 - Lorica segmentata

8b. "battle" (with PageRank)
1 - Falklands War
2 - Navy
3 - Nazi Germany
4 - Netherlands
5 - Portugal
6 - Montoneros
7 - Paolo Uccello
8 - History of the Netherlands
9 - Norway
10 - Normandy

9a. "search" (without PageRank)
1 - Natasha Stott Despoja
2 - Kaluza?Klein theory
3 - PHP-Nuke
4 - Eth
5 - Gopher (protocol)
6 - Isa (disambiguation)
7 - Lorisidae
8 - Library reference desk
9 - Geocaching
10 - Demographics of Liberia

9b. "search" (with PageRank)
1 - Netherlands
2 - New Amsterdam
3 - Pope
4 - Empress Jit?
5 - Empress Suiko
6 - Pennsylvania
7 - George Berkeley
8 - Hinduism
9 - History of the Netherlands
10 - North Pole

10a. "computer science" (without PageRank)
1 - LEO (computer)
2 - PCP
3 - Junk science
4 - Hacker (term)
5 - Malware
6 - Gary Kildall
7 - Motherboard
8 - Foonly
9 - PVC (disambiguation)
10 - Graphical user interface

10b. "computer science" (with PageRank)
1 - Portugal
2 - Islamabad Capital Territory
3 - J?rgen Habermas
4 - Mercury (planet)
5 - Isaac Asimov
6 - Malware
7 - LEO (computer)
8 - Pakistan
9 - O
10 - John von Neumann