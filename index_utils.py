def create_vocabulary(path_tsv):
    for file in sorted(os.listdir(path_tsv)):#iteration over files
        if file.startswith ("article_"): #check file is an article
            with open(path_tsv+file, "r", encoding = "utf-8") as f:
                text = f.read().lower() # read the file and trasform it in lowercase
                words=cleaner(text) #--> func: cleaner
                for w in words:
                    if vocab.get(w, None)==None:#if v not in vocabulary:
                        vocab[w]=len(vocab) #add it

def cleaner(text):#input: a text to be clean:
                    #output: a list of words of the text cleaned

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

def number_document_html(file):#input: the name of the document; easy to obtain.. it's the file in: file in sorted(os.listdir(path))
    if type(file)!=str:
        raise Exception('file must have type str; {} obtained.'.format(type(file)))
    start=len('article_')
    return(int(file[start:-5])) #output: the number of the file

def numer_document_tsv(file):#input: the name of the document; easy to obtain.. it's the file in: file in sorted(os.listdir(path))
    if type(file)!=str:
        raise Exception('file must have type str; {} obtained.'.format(type(file)))
    start=len('article_')
    return(int(file[start:-4])) #output: the number of the file

def cleaner_tsv_files_update_index(path_tsv): #input: the path where the file tsv are
    for file in sorted(os.listdir(path_tsv)):
        #print('sto pulendo il file: {}'.format(file))
        if file.startswith("article_"):
            with open(path_tsv+file, "r", encoding = "utf-8") as f:
                text = f.read().lower() # read the file
                clean_text_words=cleaner(text) #clean the text
                updateIndex(clean_text_words, file) #--> updateIndex

def updateIndex(listOfWords, fileName):
    num_doc=numer_document_tsv(fileName) #retrive the number of the file
    for word in listOfWords:
        num_word=vocab[word] #retrive the number of the word
        posts=index.get(num_word, None)#try to obtain the value of the word key:
        if posts==None: #if it is absent
            index[num_word]={num_doc:1} #add the key with value a dictionary{doc: frequenzy}
        else:
            post=index[num_word].get(num_doc, None)# otherwise try to obtain the value of the document key
            if post==None: #if it's absent:
                index[num_word][num_doc]=1 #add the document key with frequency 1
            else:
                index[num_word][num_doc]+=1#:otherwise update the last value
