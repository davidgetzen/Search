from Indexer import Indexer
if __name__ == "__main__":
    indexer = Indexer("wikis/SmallWiki.xml", "title_file.txt")
    print(indexer.parse_xml())
    # while True:
    # user_text = input("Please enter a string (or type :q to leave the program): ")
    # if user_text == ":q":
    #     break
    # print(user_text.upper()) # This is where we should call the helper for the querier.