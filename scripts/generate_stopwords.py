#!/usr/bin/python

import os
import pickle
import re
import string
import stop_words
from dotenv import load_dotenv
import unidecode


def clean_text(text):
    return unidecode.unidecode(re.sub(r'http\S+', '', text.strip().lower(), flags=re.MULTILINE))


load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app/.env'))
stopwords = []

stopwords_dir = os.getenv('GENERATOR_STOPWORDS_DIRECTORY')
directory = os.fsencode(stopwords_dir)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    with open(stopwords_dir + filename, 'r') as f:
        stopwords += [clean_text(word) for word in f.read().splitlines() if clean_text(word) not in stopwords]

stopwords += string.punctuation
stopwords += ['soria']
stopwords += stop_words.get_stop_words('es')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.getenv('STOPWORDS_FILE')), 'wb') as fp:
    print(len(stopwords))
    pickle.dump(stopwords, fp)
