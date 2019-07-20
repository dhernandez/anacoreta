import datetime
import hashlib
import json
import os

from app.utils.utils import clean_text


class Files:
    @staticmethod
    def save(source, date, text):
        data = {
            'source': source,
            'date': str(date),
            'text': clean_text(text),
        }

        file_full_path = os.getenv('SOURCES_DIRECTORY') + '{}_{}_{}'.format(source, date,
                                                                            hashlib.sha3_224(
                                                                                text.encode('utf-8')).hexdigest())
        with open(file_full_path, 'w') as outfile:
            print('Saving article from {}. Date: {}'.format(source, str(date)))
            json.dump(data, outfile)

    @staticmethod
    def get_last_texts(minutes):
        now = datetime.datetime.now()
        trendings_from = now - datetime.timedelta(minutes=minutes)
        recent_texts = []
        directory = os.fsencode(os.getenv('SOURCES_DIRECTORY'))
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            with open(os.getenv('SOURCES_DIRECTORY') + filename) as json_file:
                data = json.load(json_file)
                try:
                    if datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S') > trendings_from:
                        recent_texts.append(data['text'])
                except:
                    pass
        return recent_texts
