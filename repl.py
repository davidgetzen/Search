from index import index
from query import Querier

if __name__ == "__main__":
    #indexer = index("wikis/MedWiki.xml", "title_file.txt", "words_file.txt", "docs_file.txt")
    #indexer.parse_xml()
    querier = Querier("title_file.txt", "docs_file.txt", "words_file.txt", True)
    querier.start_querying("lycée lyautey")
    
    # while True:
    # user_text = input("Please enter a string (or type :q to leave the program): ")
    # if user_text == ":q":
    #     break
    # print(user_text.upper()) # This is where we should call the helper for the querier.
