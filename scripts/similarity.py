import pandas as pd
import numpy as np
from flask import jsonify
import nltk

from contractions import fix
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords #4
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

import regex as re

"""
Search for TODO
"""

disease_symptom_list = []
input_file_name = 'data/dataset.csv'
threshold = 0
vocab = set()

##################################################################################################



def readData(inpit_file_name):
    data_df = pd.read_csv(input_file_name)

    return data_df


def createDiseaseSymptomDict(data_df):
##################################################################################################
    """
    TODO
    create a list of dicts with each dictionary having the structure give as follows :
        {
            'name': name_of_disease,
            'symptom_list': symptom_list,
            'token_list': list_of_tokens (to be generated from symptoms list), HINT : " ".join(symptom_list)
            'similarity_score': 0.0 (initialize score to 0.0), will be computed when user submits query)
        }
    input : data frame -> cols : Name, names of symptoms,
    functionality : traverse over dataframe, create symptom list for every disease, create token list by calling text preprocessing
    output : disease_symptom_list (list of dicts ('str' : value, value is float, list, str))
    eg :
    disease_symptom_list = [
        {
            name : 'A',
            'symptom_list' : ['pain - is', 'is - Ache'],
            'token_list' : ['pain', 'ache'],
            'similarity_score' : 0.0
        },
        {
            name : 'B',
            'symptom_list' : ['Gain - is'],
            'token_list' : ['gain'],
            'similarity_score' : 0.0
        }
    ]
    """
    dictlist = []
    sf= data_df.keys()
    # print(sf)
    data_df = data_df.reset_index()  # make sure indexes pair with number of rows
    for index, row in data_df.iterrows():
      name=row["Name"]
      symptoms_list = []
      token_list_string = ""
      for column in data_df.columns[1:]:
        x= row[column]
        if(x==1):
          symptoms_list.append(column)
          token_list_string = token_list_string + " " + column
      token_list = textPreprocessing(token_list_string)
      thisdict={}
      thisdict.update({'name': name})
      thisdict.update({'symptom_list': symptoms_list})
      thisdict.update({'token_list': token_list})
      thisdict.update({'similarity_score': "0.0"})
      dictlist.append(thisdict)
    return dictlist

##################################################################################################

def textPreprocessing(data):
##################################################################################################
    """
    TODO
    input: data (str)
        e.g. : 'I am not feeling good !!'
    function:
        Perform these
            1. case generalization // make everything lower case
            2. contraction removal //use data = contractions.fix(data)
            3. punctuation removal. // remove - and most other punctuations
            4. tokenaization // use reference from MNIST
            5. lemmetization // look up online
            6. stop words removal // use reference from MNIST
        return a list of tokens
    output:
        list of tokens (list of str)
        e.g. " ['feel', 'good']
    """
    # YOUR CODE GOES HERE, REMOVE PASS
    
    data = data.lower() #1
    data = fix(data) #2
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' #3
    for l in data:
      for ele in punc:
        if l in punc:
          data = data.replace(l, "")
    nltk.download('stopwords', quiet = True)
    stop_words = list(stopwords.words('english'))
    nltk.download('punkt', quiet = True)
    tokenized_text = nltk.word_tokenize(data)
    tokenized_text_after_stopwords_removal = [word for word in tokenized_text if word not in stop_words]
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    wl = WordNetLemmatizer()
    
    lemmas_of_speech_words = [wl.lemmatize(word) for word in tokenized_text_after_stopwords_removal]
    # print(lemmas_of_speech_words)
    return lemmas_of_speech_words


##################################################################################################



from math import sqrt
def cosineSimilarity(a, b):

    # IMP do not alter
    global vocab

##################################################################################################

    """
    TODO

    global vocab -> set of strs, consists set of all tokens from all diseases
    should not be altered

    input : two token lists (list of str)
        e.g. a -> ['body', 'mass'], b -> ['age', 'body']

    function :
    create a combined set from vocab and query token_list (do not alter vocab)
    calucate cosine similarity for list 'a' & 'b'
    ROUND the result to three decimals

    output : float (rounded to 3 decimal places)
        e.g. 0.023
    """

    # YOUR CODE GOES HERE, REMOVE PASS    
    num, d1, d2 = 0, 0, 0

    set_a = set(a)
    set_b = set(b)

    union = set_a.union(set_b)

    for word in union:

      if word in set_a and word in set_b:
        num+=1
        d1+=1
        d2+=1
      elif word in set_a:
        d1+=1
      elif word in set_b:
        d2+=1

    return round(num/sqrt(d1**2*d2**2),3)




##################################################################################################


def calculateTopSimilarDisease(token_list):
    global disease_symptom_list

    for disease in disease_symptom_list:
        disease['similarity_score'] = cosineSimilarity(disease['token_list'], token_list)

    disease_symptom_list = sorted(disease_symptom_list, key=lambda x: x['similarity_score'], reverse=True)


def findTopMatches(data):
    global disease_symptom_list
    global threshold

    data_token_list = textPreprocessing(data=data)

    calculateTopSimilarDisease(token_list=data_token_list)

    count = 0

    if (disease_symptom_list[0]['similarity_score'] <= threshold):
        count = 0

    else:
        count = 3

    return jsonify({'count': count, 'disease_list': disease_symptom_list[:3]})


def load():
    global disease_symptom_list
    global vocab

    data_df = readData(inpit_file_name=input_file_name)
    disease_symptom_list = createDiseaseSymptomDict(data_df=data_df)

    for disease in disease_symptom_list:

        vocab = vocab.union(set(disease['token_list']))


if (__name__ == '__main__'):
    load()

    print(disease_symptom_list)
