from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk import sent_tokenize
import string
import os
import pickle
import nltk
#nltk.download('stopwords') #decomment this lines if same errors tell to download this library
#nltk.download('punkt')
import csv
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
import os
import math
import heapq
import numpy as np
import header as h


from utils import cleaner
from utils import number_document_html

def create_vocabulary(vocab, path_tsv):#input: the (string) path to the folder that contains the tsv files
    for file in sorted(os.listdir(path_tsv)):#iteration over files
        if file.startswith ("article_"): #check file is an article
            with open(path_tsv+file, "r", encoding = "utf-8") as f:
                text = f.read().lower().split("\t") # read the file and trasform it in lowercase (to avoid to have to words in the case Tree and tree)
                words = cleaner(" ".join(text)) # Let's do the preprocessing for the inverted index for the current file
                for w in words:
                    if vocab.get(w) == None: #if the word is not in the vocabulary
                        vocab[w] = len(vocab) # add it as key, and as value put the len of the vocabulary at that oment (so it is univocal),
                                               # We do in this way so the big O is 1, because the length is already in memory


def numer_document_tsv(file):#input: the name of the document; easy to obtain.. it's the file in: file in sorted(os.listdir(path))
    if type(file)!=str:
        raise Exception('file must have type str; {} obtained.'.format(type(file)))
    start=len('article_')
    return(int(file[start:-4])) #output: the number of the file

def cleaner_tsv_files_update_index(vocab, index, path_tsv): #input: the path where the file tsv are
    for file in sorted(os.listdir(path_tsv)):
        #print('sto pulendo il file: {}'.format(file))
        if file.startswith("article_"):
            with open(path_tsv+file, "r", encoding = "utf-8") as f:
                text = f.read().lower().split("\t") # read the file
                clean_text_words = cleaner(" ".join(text[1:3])) #clean the text
                updateIndex(vocab, index, clean_text_words, file) #--> updateIndex

def cleaner_tsv_files_update_index_2(vocab, index1, index2, path_tsv): #input: the path where the file tsv are

    for file in sorted(os.listdir(path_tsv)):

        if file.startswith("article_"):
            with open(path_tsv + file, "r", encoding = "utf-8") as f:
                text = f.read().lower() # read the file and convert in lower case
                clean_text_words = cleaner(text) # Clean the text
                updateIndex_2(vocab, index1, index2, clean_text_words, file) #--> updateIndex

def get_tfidf(index1, listOfWords, num_word, num_doc):

    # Let's calculate the tf:

    try:
        freq_in_doc = index1[num_word][num_doc] # The shpae of index1 is {word_id: {document_n: frequency of the word in document n}}
        num_of_words_in_doc = len(listOfWords) # Just count the total number of word in the list

        tf = freq_in_doc/num_of_words_in_doc

        # Let's caclulate the idf

        num_docs = 30000 # Let's calculate the number of documents in the collection
        num_docs_with_w = len(index1[num_word]) # Each key of the inverted index contains all documents in which there is the word corresponding to the key of the main dict

        idf = math.log10(num_docs/num_docs_with_w)
    except:
        return 0

    return float(round(tf*idf, 9))

def cleaner_tsv_files_update_index_3(vocab, frequency_dic, index, path_tsv): #input: the path where the file tsv are

    for file in sorted(os.listdir(path_tsv)):

        if file.startswith("article_"):
            with open(path_tsv + file, "r", encoding = "utf-8") as f:

                text = f.read().lower().split("\t") # read the file and convert in lower case
                clean_text_words = cleaner(" ".join(text)) # Clean the text
                updateIndex_3(vocab, frequency_dic, index, clean_text_words, file) #--> updateIndex

def updateIndex_3(vocab, frequency_dic, index_3, listOfWords, fileName):

    num_doc = numer_document_tsv(fileName) # Retrive the number of the file

    for word in listOfWords:

        num_word = vocab[word] # Retrive the number of the word

        posts = index_3.get(num_word) # Try to obtain the value of the word key from the inverted index (key of the main dict)
        if posts == None: #if it is absent
            index_3[num_word] = {num_doc: 0} #add the key with value a dictionary {selected document: frequency in that document}
        else:
            post = index_3[num_word].get(num_doc) # otherwise try to obtain the value of the document key
            if post == None: #if it's absent:
                index_3[num_word][num_doc] = 0 #add the document key with frequency 1 (numbe rof times that that word occur in that document)

        posts_freq = frequency_dic.get(num_word)
        if posts_freq == None:
            frequency_dic[num_word] = {num_doc: [1, len(listOfWords)]} # (frequency of the wor in the doce, words in the doc)
        else:
            post = frequency_dic[num_word].get(num_doc) # otherwise try to obtain the value of the document key
            if post == None: #if it's absent:
                frequency_dic[num_word][num_doc] = [1, len(listOfWords)] #add the document key with frequency 1 (numbe rof times that that word occur in that document)
            else:
                frequency_dic[num_word][num_doc][0] += 1 #:otherwise increase the frequency

def updateIndex_2(vocab, index1, index2, listOfWords, fileName):

    num_doc = numer_document_tsv(fileName) # Retrive the number of the file

    for word in listOfWords:

        num_word = vocab[word] # Retrive the number of the word
        tfIdf = get_tfidf(index1, listOfWords, num_word, num_doc)


        posts = index2.get(num_word) # Try to obtain the value of the word key from the inverted index (key of the main dict)
        if posts == None: #if it is absent
            index2[num_word] = {num_doc: tfIdf} #add the key with value a dictionary {selected document: frequency in that document}
        else:
            post = index2[num_word].get(num_doc) # Check if the document is already under that key

            if post==None: #if it's absent:
                index2[num_word][num_doc] = tfIdf # Add the document and its tfidf

def updateIndex(vocab, index, listOfWords, fileName):
    num_doc=numer_document_tsv(fileName) #retrive the number of the file
    for word in listOfWords:
        num_word = vocab[word] #retrive the number of the word
        posts = index.get(num_word) #try to obtain the value of the word key:
        if posts == None: #if it is absent
            index[num_word] = {num_doc: 1} #add the key with value a dictionary{doc: frequency}
        else:
            post = index[num_word].get(num_doc)# otherwise try to obtain the value of the document key
            if post == None: #if it's absent:
                index[num_word][num_doc] = 1 #add the document key with frequency 1 (numbe rof times that that word occur in that document)
            else:
                index[num_word][num_doc] += 1 #:otherwise update the last value


def compile_tfidf(index_3, frequency_dic):

    for key, value in frequency_dic.items():
        for doc, lst in value.items():

            num_word = key
            num_doc = doc
            w_freq = lst[0]
            len_doc = lst[1]

            tf = w_freq/len_doc
            idf = 30000/len(index_3[num_word])

            tfIdf = tf*idf

            index_3[num_word][num_doc] = round(tfIdf, 9)
