if __name__ == "__main__":
    while True:
        user_text = input("Please enter a string (or type :q to leave the program): ")
        if user_text == ":q":
            break
        print(user_text.upper()) # This is where we should call the helper for the querier.
        