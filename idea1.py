import pandas as pd
import os
import sys
import nltk
from nltk.corpus import words
from nltk.stem import PorterStemmer
import random
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

#constants
data = sys.argv[1] #folder with all the data
wrds = set(words.words())
ps = PorterStemmer()
genre_dict = {"Country": 0, "Electronic": 1, "Folk": 2,
"Hiphop": 3, "Indie": 4, "Jazz": 5, "Metal": 6,
"Pop": 7, "R&B": 8, "Rock": 9}

#methods
#method create a pd dataframe with all the songs
def fill_song_pd():
    df = pd.DataFrame(columns = ["lyrics", "genre"])
    #open each folder
    i = 0
    for folder in os.listdir(data):
        f = os.path.join(data, folder)
        for file in os.listdir(f):
            path = os.path.join(f,file)
            with open(path, encoding = 'utf-8') as fl:
                #cleaning data, remove all songs w/ invalid length
                length = 0
                lyrics = fl.read()
                for w in nltk.word_tokenize(lyrics):
                    length +=1
                if length < 100 or length >= 800:
                    continue
                #if length is fine, add to panda
                else:
                    df.loc[i] = [lyrics] + [genre_dict[folder]]
                    i+=1
                    fl.close()
    return df

df = fill_song_pd()
#method gets list of words common to specific genre
def get_wrd_list(genre):
    list = []
    for index, row in df.iterrows():
        if row['genre'] == genre_dict[genre]:
            list.append(row['lyrics'].lower())

    random.shuffle(list)
    cv_list = list[0: int(len(list)/3)]
    cv = CountVectorizer(input = 'content', ngram_range = (1,2))
    cv.fit(cv_list)
    #return list of features
    return cv.get_feature_names()

#method gets part of speach percentages for each genre
def get_pos_pctg(genre):
    total_len = 0
    dict = {} #keys are POS, values are number of words w/ POS tag
    for index, row in df.iterrows():
        if row['genre'] == genre_dict[genre]:
            for w in word_tokenize(row['lyrics']):
                total_len +=1
                pos = nltk.pos_tag(w)
                tuple = pos[0]
                if tuple[1] not in dict.keys(): #adds new POS to dict if not in there
                    dict[tuple[1]] = 1
                else:
                    dict[tuple[1]] = dict[tuple[1]] + 1 #updates value
    #convert values to percentages
    for key in dict.keys():
        dict[key] = dict[key]/total_len
    return dict

"""method creates a panda that has the features of each genre
rows are genres, cols are features"""
def fill_genre_pd():
    df2 = pd.DataFrame(columns = ["word list", "POS perctg"])
    wrd_lists = [] #going to be a list of wrd_lists
    for genre in genre_dict.keys():
        wrd_list = list(get_wrd_list(genre))
        wrd_lists.append(wrd_list)
    #making each list only contain its unique words
    for w_list in wrd_lists:
        union = set(w_list)
        for l in wrd_lists:
            if l != w_list:
                union = union and set(l)
        w_list = list(set(w_list) - union)

    i = 0
    for genre in genre_dict.keys():
        df2.loc[i] = [wrd_lists[i]] + [get_pos_pctg(genre)]
        i+=1

    print(df2.head(10))


fill_genre_pd()
