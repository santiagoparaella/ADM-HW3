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
import re
import math
import heapq
import numpy as np
import header as h
from scipy.stats.stats import pearsonr


def number_document_html(file):#input: the name of the document; easy to obtain.. it's the file in: file in sorted(os.listdir(path))
    if type(file)!=str:
        raise Exception('file must have type str; {} obtained.'.format(type(file)))
    start=len('article_')
    return(int(file[start:-5])) #output: the number of the file

def cleaner(text):#input: a text to be clean:
                    #output: a list of words of the text cleaned
    text=text.lower()
    # remove remaining tokens that are not alphabetic
    clean_text="".join([ch if ch.isalnum() else " " for ch in text]) #trasform all non alnumeric character
                                                                    #into a space
    words = word_tokenize(clean_text)
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    stop_words.add('na')
    words = [w for w in words if not w in stop_words]
    # stemming of words
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in words]

    return(stemmed)

def load_urls():#return a dictionary with all urls
    with open(h.PATH_HTMLS, 'r') as f:
        line_split=[line[:-1].split('\t') for line in f.readlines()]
        urls={}
        for line in line_split:
            urls[int(line[0])]=line[1]
    return urls

def load_urls_and_vocab():
    vocab={}
    al=load_urls()

    with open(h.PATH_VOCAB, 'rb') as f:
        vocab=pickle.load(f)

    return al, vocab

def cosine_similarity(index2, vocab, query_words, doc):

    # Let's create a vector for query and documents containing the tf-idf for each word:

    query = []
    document = []
    len_q = len(query_words)

    for word in query_words: # DO it for each word

        # let's calculate tf-idf of the query:

        tf_q = query_words.count(word)/len_q
        try:
            idf_q = math.log(30000/len(index2[vocab[word]]))
        except:
            idf_q=0
        tfIdf_q = tf_q * idf_q
        query.append(tfIdf_q)

        # let's get tf-idf for the document:
        try:
            tfIdf_d = index2[vocab[word]][doc] # we have already stored the tf-idf in the index
        except:
            tfIdf_d=0
        document.append(tfIdf_d)

    # Transform the lists in an arrays:

    query_arr = np.array(query)
    document_arr = np.array(document)

    # Let's calculate the dot_product:

    dot_prod = np.dot(query_arr, document_arr)

    # Let's caclulate the norm:

    norm_q = 0
    for n in query:
        norm_q += n**2

    norm_d = 0
    for n in document:
        norm_d += n**2

    # final result:

    result = dot_prod/(math.sqrt(norm_q)*math.sqrt(norm_d))

    return round(result, 6)

def query_result(output):

    # Let's create the heap:

    heap = [(out[3], out) for out in output] # We create a list for the heap and we give as first element the one by which we want to sort the heap: [(cosine_1, [output_1])]
    heapq.heapify(heap) # Let's create the heap

    # Let's get the first k elements:

    K = 10 # We want the top 10

    k_output = heapq.nlargest(K, heap, key = lambda el: el[0]) # Get these elements from the heap (ordered by the cosine

    # Let's create the DF with the top 10 results (or if are less than 10 the results we have with no 0 similarity):

    k_out = [el[1] for el in k_output if el[1][3] != 0] # Let's extract the list with all the info from the heap.nlargest results (with a cosine not equal to 0) (see above which shape has the our heap)
    columns_name = ["Title", "Intro",  "Link", "Similarity"]

    df = pd.DataFrame(k_out, columns = columns_name) # Create the DF
    #df = df[["Title", "Intro", "Link", "Similarity"]] # Let's decide the order of columns

    return df

def pearson_correlation(index_3, vocab, query_words, doc):

    # Let's create a vector for query and documents containing the tf-idf for each word:

    query = []
    document = []
    len_q = len(query_words)

    for word in query_words: # DO it for each word

        # let's calculate tf-idf of the query:

        tf_q = query_words.count(word)/len_q
        try:
            idf_q = math.log(30000/len(index_3[vocab[word]]))
        except:
            idf_q=0
        tfIdf_q = tf_q * idf_q
        query.append(tfIdf_q)

        # let's get tf-idf for the document:
        try:
            tfIdf_d = index_3[vocab[word]][doc] # we have already stored the tf-idf in the index
        except:
            tfIdf_d=0
        document.append(tfIdf_d)

    # Transform the lists in an arrays:

    query_arr = np.array(query)
    document_arr = np.array(document)

    # Let's calculate the dot_product:

    result = pearsonr(query_arr, document_arr)[0]

    return round(result, 6)

def query_result_3(output):

    # Let's create the heap:

    heap = [(out[3], out) for out in output] # We create a list for the heap and we give as first element the one by which we want to sort the heap: [(cosine_1, [output_1])]
    heapq.heapify(heap) # Let's create the heap

    # Let's get the first k elements:

    K = 10 # We want the top 10

    k_output = heapq.nlargest(K, heap, key = lambda el: el[0]) # Get these elements from the heap (ordered by the cosine

    # Let's create the DF with the top 10 results (or if are less than 10 the results we have with no 0 similarity):

    k_out = [el[1] for el in k_output] # Let's extract the list with all the info from the heap.nlargest results (with a cosine not equal to 0) (see above which shape has the our heap)
    columns_name = ["Title", "Intro",  "Link", "Similarity"]

    df = pd.DataFrame(k_out, columns = columns_name) # Create the DF
    #df = df[["Title", "Intro", "Link", "Similarity"]] # Let's decide the order of columns

    return df

def search_engine_1(al, vocab):

    index={}
    with open(h.PATH_INDEX_1, 'rb') as f:
        index=pickle.load(f)

    query=input('Give me a query :)')

    query_words=set(cleaner(query))
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
        with open(h.PATH_TSV+name_file_tsv, 'r') as file: #open the file
            file_tsv_reader=csv.reader(file, delimiter='\t') #read it
            list_file_content=[row for row in file_tsv_reader][0]
            #print(type(list_file_content))
            out_doc.append(list_file_content[0]) #append title
            out_doc.append(list_file_content[1])#append intro
            out_doc.append(al[doc+1])

        output.append(out_doc)
    seconds=round(time.time()-start, 2)
    if len(output)>0:
        print('We have found {} results in {} second(s).'.format(len(output), seconds))
        output_df=pd.DataFrame(output, columns=['title', 'intro', 'url'])
        print(output_df)
    else:
        print('No results.')


def search_engine_2(al, vocab):
    index2={}
    with open(h.PATH_INDEX_2, 'rb') as f:
        index2=pickle.load(f)

    query=input('Give me a query :)')

    query_words=cleaner(query)
    posts_list=[]
    start=time.time()
    for word in query_words: # iterate over words
        if word in vocab.keys():#check if the word is present
            num_word=vocab[word]#retrive the number of the word
            posts_list.append(index2[num_word])#retrive the doducemnts of the word

    conjuntive_docs=set()
    posts_list.sort(key=len) #sorting by the len of the dictionary inside
    if len(posts_list)>0:
        conjuntive_docs=set(posts_list[0].keys()) #take the smallest
        for posts in posts_list[1:]: #iterate over the documents from 1 to the end
            conjuntive_docs.intersection_update(set(posts.keys())) #update the set with commons documents

    docs=list(conjuntive_docs)
    output=[]
    for doc in docs:#iterate over documents
        name_file_tsv=''.join(['article_', str(doc), '.tsv']) #obtain the name of the file
        file_tsv=None
        out_doc=[]
        with open(h.PATH_TSV+name_file_tsv, 'r') as file: #open the file
            file_tsv_reader=csv.reader(file, delimiter='\t') #read it
            list_file_content=next(file_tsv_reader)#read the only one line
            #print(type(list_file_content))

            out_doc.append(list_file_content[0]) #append title
            out_doc.append(list_file_content[1])#append intro
            out_doc.append(al[doc+1])
            out_doc.append(cosine_similarity(index2, vocab, query_words, doc))
            #print(cosine_similarity(query_words, doc))

        output.append(out_doc)

    seconds=round(time.time()-start, 2)

    if len(output)>0:
        print('We have found {} results in {} second(s).'.format(len(output), seconds))
        print(query_result(output))
    else:
        print('No results.')


def search_engine_3(al, vocab):
    index_3={}
    with open(h.PATH_INDEX_3, 'rb') as f:
        index_3=pickle.load(f)

    query=input('Give me a query :)')

    query_words=cleaner(query)

    while len(query_words)<2:
        print('For the Pearson Correlation you must give more words; \nPlease, retry')
        query=input('Give me a query :)')
        query_words=cleaner(query)

    posts_list=[]
    start=time.time()
    for word in query_words: # iterate over words
        if word in vocab.keys():#check if the word is present
            num_word=vocab[word]#retrive the number of the word
            posts_list.append(index_3[num_word])#retrive the doducemnts of the word

    conjuntive_docs=set()
    posts_list.sort(key=len) #sorting by the len of the dictionary inside
    if len(posts_list)>0:
        conjuntive_docs=set(posts_list[0].keys()) #take the smallest
        for posts in posts_list[1:]: #iterate over the documents from 1 to the end
            conjuntive_docs.intersection_update(set(posts.keys())) #update the set with commons documents

    docs=list(conjuntive_docs)
    output=[]
    for doc in docs:#iterate over documents
        name_file_tsv=''.join(['article_', str(doc), '.tsv']) #obtain the name of the file
        file_tsv=None
        out_doc=[]
        with open(h.PATH_TSV+name_file_tsv, 'r') as file: #open the file
            file_tsv_reader=csv.reader(file, delimiter='\t') #read it
            list_file_content=next(file_tsv_reader)#read the only one line
            #print(type(list_file_content))

            out_doc.append(list_file_content[0]) #append title
            out_doc.append(list_file_content[1])#append intro
            out_doc.append(al[doc+1])
            out_doc.append(pearson_correlation(index_3, vocab, query_words, doc))
            #print(cosine_similarity(query_words, doc))

        output.append(out_doc)

    seconds=round(time.time()-start, 2)

    if len(output)>0:
        print('We have found {} results in {} second(s).'.format(len(output), seconds))
        print(query_result_3(output))
    else:
        print('No results.')
