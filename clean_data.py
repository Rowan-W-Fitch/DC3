from langdetect import detect
import os
import sys
import nltk
from nltk import word_tokenize

data = sys.argv[1]
del_list = []
for folder in os.listdir(data):
    fold = os.path.join(data,folder)
    for file in os.listdir(fold):
        with open(os.path.join(fold,file), encoding = 'utf-8') as f:
            non_english = 0
            length = 0
            lyrics = f.read()
            for w in nltk.word_tokenize(lyrics):
                length +=1
            if length < 100 or length >= 800:
                del_list.append(os.path.join(fold,file))
            elif detect(lyrics) != 'en':
                del_list.append(os.path.join(fold,file))

for dir in del_list:
    os.remove(dir)
