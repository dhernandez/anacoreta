import os
from textblob import TextBlob
import numpy as np

from app.storage.StorageManager import StorageManager

STOPWORDS_DIR = os.getenv('STOPWORDS_DIRECTORY')
SOURCES_DIR = os.getenv('SOURCES_DIRECTORY')


def get_sentiment():
    recent_texts = StorageManager.get_last_texts(float(os.getenv('MINUTES_FOR_EXTRACT_TRENDINGS')))
    polarities = []

    for text in recent_texts:
        blob = TextBlob(text)
        polarities += [blob.polarity] if blob.polarity != 0.0 else []
        try:
            sentences, polarity = zip(*[(str(sentence), sentence.sentiment.polarity) for sentence in blob.sentences if sentence.sentiment.polarity != 0.0])
            print('Sentiment average: {}'.format(np.mean(polarity)))
        except ValueError as error:
            pass

    mean = np.mean(polarities)
    print('Total sentiment average: {}'.format(mean))
    return mean
