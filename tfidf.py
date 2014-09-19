import nltk
from collections import Counter
from nltk import word_tokenize
from os import listdir
import math
from os.path import isfile, join
from nltk.corpus import stopwords
lemma = nltk.WordNetLemmatizer()

'''
    Modified implementation of TFIDF for when each line of a file represents a
    unique document.
'''

def tokenize_string(string) :
    toks = word_tokenize(string)
    toks = [w.lower().replace('.','') for w in toks if pass_filters(w)]
    toks = [lemma.lemmatize(t) for t in toks]
    return toks

def pass_filters(tok) :
    filters = [lambda w : w in stopwords.words('english'),  #Ignore stopwords
                lambda w : len(w) == 0,                     #Empty Token
                lambda w : w == '``' or w == "''",          #Another form of noisy token
                lambda w : len(w) == 1 and not str.isalnum(w[0])] #Single punctuation tokens
    for test in filters :
        if test(tok) :
            return False
    return True

class TFIDF : 
    def count_freq(self, term, val) :
        ''' Update term frequency '''
        if self.term_freq.has_key(term) :
            self.term_freq[term] += val
        else :
            self.term_freq[term] = val

    def count_doc(self, term) :
        ''' Update document frequency '''
        if self.term_docnum.has_key(term) :
            self.term_docnum[term] += 1
        else :
            self.term_docnum[term] = 1

    def __init__(self, document_list) :
        '''
            The "document list" is expected to be a list, where each element
            represents a document. A document is expressed as a list of tokens.
            The input to this constructor then, is a list of list of tokens.
        '''
        self.term_docnum = dict()
        self.term_freq = dict()

        self.num_docs = len(document_list)
        for doc in document_list :
            freq_dict = Counter(doc)
            for item in freq_dict.items() :
                # ITEM : (Key, Freq)
                self.count_freq(item[0], item[1])
                self.count_doc(item[0])
        self.ordered_term_frequency = sorted(self.term_freq.items(), \
                key=lambda x : x[1], reverse = True)
        self.max_freq = self.ordered_term_frequency[0][1]

    def tf_idf(self, term) :
        ''' Calculate tf-idf for a term, based on training corpus.  '''
        if not (self.term_docnum.has_key(term) and self.term_freq.has_key(term)) :
            ''' If frequency is zero, the TF/IDF is always 0.5 (divide by zero for
            IDF)'''
            return 0
        tf = 0.5 + float(0.5*self.term_freq[term]) / float(self.max_freq)
        idf = math.log(self.num_docs/float(self.term_docnum[term]),2)
        return tf*idf
