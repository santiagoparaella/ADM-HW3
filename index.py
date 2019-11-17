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

from index_utils import create_vocabulary
from utils import cleaner
from utils import number_document_html
from index_utils import numer_document_tsv
from index_utils import cleaner_tsv_files_update_index
from index_utils import cleaner_tsv_files_update_index_2
from index_utils import cleaner_tsv_files_update_index_3
from index_utils import updateIndex
from index_utils import compile_tfidf


import header as h


#vocabulary creation

vocab = {}

create_vocabulary(vocab, h.PATH_TSV) #--> function create_vocabulary
print('creation vocabolary done!')

with open(h.PATH_VOCAB, 'wb') as f: #set your path to save index
        pickle.dump(vocab, f, pickle.HIGHEST_PROTOCOL) # open and save vocabulary into a file
print('Vocabulary saved!')

# index 1 creation

index={}

with open(h.PATH_VOCAB, 'rb') as f: #set your path to save index
        vocab=pickle.load(f) # load vocabulary
print('Vocabulary loaded!')


print('next function can take saveral minutes; please wait...')
cleaner_tsv_files_update_index(vocab, index, h.PATH_TSV) #cleane tsv file
print('inverted index 1 creato correttamete!')


with open(h.PATH_INDEX_1, 'wb') as f: # and save index into a file
        pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)
print('invert index 1 salvato correttamete!')



# index 2 creation
index2={}
index1={}

with open(h.PATH_INDEX_1, 'rb') as f:
    index1=pickle.load(f)
with open(h.PATH_VOCAB, 'rb') as f:
    vocab=pickle.load(f)

cleaner_tsv_files_update_index_2(vocab, index1, index2, h.PATH_TSV) #cleane tsv file
print('inverted index 2 creato correttamete!')


with open(h.PATH_INDEX_2, 'wb') as f: # and save index into a file
        pickle.dump(index2, f, pickle.HIGHEST_PROTOCOL)
print('invert index 2 salvato correttamete!')

#index 3 creation
index3={}
with open(h.PATH_VOCAB, 'rb') as f:
    vocab=pickle.load(f)

frequency_dic = {} # it stores the frequrncies needed to calculate tf-idf
cleaner_tsv_files_update_index_3(vocab, frequency_dic, index3, h.PATH_TSV) #cleane and prepare tsv file for the index 2
compile_tfidf(index3, frequency_dic) # Add the tfidf

print('Inverted Index 3 completed')


with open(h.PATH_INDEX_3, 'wb') as f: # and save index into a file
    pickle.dump(index3, f, pickle.HIGHEST_PROTOCOL)
print('Inverted Index 3 saved')
