# ADM-HW3

This repository contains all files about the homework 3 of ADM course.
We are the group 5 composed by:

* *Palaia Santo* (1611683 - palaia.1611683@studenti.uniroma1.it)
* *Dario russo* (1714011 - russo.1714011@studenti.uniroma1.it)
* *Melika parpinchi* (1880156 - galexyp2008@gmail.com)

Following you can find an explanation of all files in this repository:

* `(this)README.md`: a Markdown file that explains the content of this repository. As we are doing it explain for all file what it contains.

* `header.py`: a oython file that contains the costants of the HW.

* `collector.py`: a python file that contains the line of code needed to collect our data from the `html` page (from which you get the urls) and Wikipedia.
* `collector_utils.py`: a python file that stores the function we used in `collector.py`.
* `parser.py`: a python file that contains the line of code needed to parse the entire collection of `html` pages and save those in `tsv` files.
* `parser_utils.py`: a python file that gathers the function we used in `parser.py`.
* `index.py`: a python file that once executed generate the indexes of the Search engines.
* `index_utils.py`: a python file that contains the functions you used for creating indexes.
* `utils.py`: a python file that gather functions we need in more than one of the previous files like (`collector`, `parser`, etc.)
* `main.py`: a python file that once executed build up the search engine and allow you to execute a query. When you (or an user) executes the file you should be able to choose:
	* `search_engine`: a parameter that the user set to choose the search engine to run. According to the request of the homework, you can get 1,2 or 3.
* `exercise_4.py`: python file that contains the implementation of the algorithm that solves problem 4.

* `main.ipynb`: a Jupyter notebook explaines the strategies our adopted solving the homework.

This repository also contains:
* `vocabulary.pkl`: a pickle file that contains the vocabulary 
* `movieTot.txt`: a text file with the wole urls
* `inverted_index.pkl`,`inverted_index2.pkl`,`inverted_index3.pkl`: the indices to build up our three search engine
