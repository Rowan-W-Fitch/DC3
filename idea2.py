import sys
import os
import pandas as pd
import nltk
from pymarkovchain import MarkovChain
from nltk import word_tokenize
#constants
data = sys.argv[1] #folder with all the data
genre = sys.argv[2] #the genre you want (must match spelling and capitalization of the folder names)
lines = sys.argv[3] #number of lines of lyrics you want
genre_dict = {"Country": 0, "Electronic": 1, "Folk": 2,
"Hiphop": 3, "Indie": 4, "Jazz": 5, "Metal": 6,
"Pop": 7, "R&B": 8, "Rock": 9}
#methods
#method creates a pandas dataframe with the songs as rows, lyrics and genre are columns
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

#this method uses the markov chain package to generate random lyrics
def main():
    df = fill_song_pd()
    lyrics = "" #going to be one huge string
    db_name = './markov/' + genre
    mc = MarkovChain(db_name)
    #creating new markov dataset if it doesn't exist
    if not os.path.isfile(db_name):
        print("creating new data set based on the " + str(genre) + " genre...")
        for index,row in df.iterrows():
            if row['genre'] == genre_dict[genre]:
                lyrics += row["lyrics"] + " "
            mc.generateDatabase(lyrics)
            mc.dumpdb()

    for i in range(int(lines) + 1):
        print(mc.generateString())

main()
