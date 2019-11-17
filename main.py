import utils as u

if __name__ == "__main__":


    al, vocab=u.load_urls_and_vocab()

    choice_done = True
    while choice_done:

        which_engine = input("Choose with which Search Engine you want to do your research: \n1 - Engine 1 \n2 - Engine 2 \n3 - Engine 3 \nq - Quit \n\n")

        if which_engine == "1":
            u.search_engine_1(al, vocab)
        elif which_engine == "2":
            u.search_engine_2(al, vocab)
        elif which_engine == "3":
            u.search_engine_3(al, vocab)
        elif which_engine.lower() == "q":
            print("Goodbye!")
            choice_done = False
        else:
            print("No result for this choice. \nTry Again!\n")
