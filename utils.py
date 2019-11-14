import pickle
import csv
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk import sent_tokenize
import json
import time

def cleaner(text):#input: a text to be clean:
                    #output: a list of words of the text cleaned
    text=text.lower()
    # remove remaining tokens that are not alphabetic
    clean_text="".join([ch if ch.isalnum() else " " for ch in text]) #trasform all non alnumeric character
                                                                    #into a space
    words = word_tokenize(clean_text)
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    # stemming of words
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in words]

    return(stemmed)

def search_engine_1():

    vocab={}
    index={}
    al=[]

    path_vocab='/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/vocabulary.pkl'
    path_index='/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/inverted_index.pkl'
    path_tsv='/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/fileTsv/'
    path_html='/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/htmls.txt'


    with open(path_index, 'rb') as f:
        index=pickle.load(f)
    with open(path_vocab, 'rb') as f:
        vocab=pickle.load(f)
    with open(path_html, 'r') as f:
        al=json.loads(f.read())

    query=input('Give me a query :)')

    query_words=cleaner(query)
    posts_list=[]
    start=time.time()
    for word in query_words: # iterate over words
        if word in vocab.keys():#check if the word is present
            num_word=vocab[word]#retrive the number of the word
            posts_list.append(index[num_word])#retrive the doducemnts of the word

    conjuntive_docs=set()
    posts_list.sort(key=len) #sorting by the len of the dictionary inside
    if len(posts_list)>0:
        conjuntive_docs=set(posts_list[0]) #take the smallest
        for posts in posts_list[1:]: #iterate over the documents from 1 to the end
            conjuntive_docs.intersection_update(set(posts.keys())) #update the set with commons documents

    docs=list(conjuntive_docs)
    output=[]
    for doc in docs:#iterate over documents
        name_file_tsv=''.join(['article_', str(doc), '.tsv']) #obtain the name of the file
        file_tsv=None
        out_doc=[]
        with open(path_tsv+name_file_tsv, 'r') as file: #open the file
            file_tsv_reader=csv.reader(file, delimiter='\t') #read it
            list_file_content=next(file_tsv_reader)#read the only one line
            #print(type(list_file_content))
            out_doc.append(list_file_content[0]) #append title
            out_doc.append(list_file_content[1])#append intro
            out_doc.append(al[doc])

        output.append(out_doc)
    seconds=round(time.time()-start, 2)
    if len(output)>0:
        print('We have found {} results in {} second(s).'.format(len(output), seconds))
        output_df=pd.DataFrame(output, columns=['title', 'intro', 'url'])
        print(output_df)
    else:
        print('No results.')
