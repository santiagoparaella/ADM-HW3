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

from index_utils import create_vocabulary
from index_utils import cleaner
from index_utils import number_document_html
from index_utils import numer_document_tsv
from index_utils import cleaner_tsv_files_update_index
from index_utils import updateIndex

#vocabulary creation

vocab={}
path='/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/fileTsv/' #set the path to your tsv folder
print('next function can take several minutes; please wait...')
create_vocabulary(path) #--> function create_vocabulary
print('creation vocabolary done!')
with open('/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/vocabulary.pkl', 'wb') as f:#set your path to save index
        pickle.dump(vocab, f, pickle.HIGHEST_PROTOCOL) #open and safe vocabulary into a file
print('vocabolario salvato correttamete!')

# index creation

index={}
path_tsv='/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/fileTsv/'
path_index='/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/inverted_index.pkl'
#set your path

print('nexr function can take saveral minutes; please wait...')
cleaner_tsv_files_update_index(path_tsv) #cleane tsv file
print('inverted index creato correttamete!')


with open(path_index, 'wb') as f: # and save index into a file
        pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)
print('invert index salvato correttamete!')
