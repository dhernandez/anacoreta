import os
import pickle
import re
import unidecode as unidecode


def clean_text(text):
    return unidecode.unidecode(re.sub(r'http\S+', '', text.strip().lower(), flags=re.MULTILINE))


def get_stopwords():
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.getenv('STOPWORDS_FILE')), 'rb') as fp:
        return pickle.load(fp)
