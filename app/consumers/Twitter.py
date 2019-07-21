import datetime
import json
import os
import threading
import tweepy

from app.tasks.send_updates import send_updates
from app.storage.StorageManager import StorageManager


class Twitter(threading.Thread):
    DIRECTORY = os.getenv('SOURCES_DIRECTORY')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    ACCESS_SECRET = os.getenv('ACCESS_SECRET')
    FILENAME_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    ORIGINAL_TIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'
    CITY_LOCATIONS = [float(point) for point in os.getenv('CITY_LOCATIONS').split(',')]

    class MyStreamListener(tweepy.streaming.StreamListener):
        def on_status(self, status):
            print('Tuit received')
            StorageManager.save(
                'twitter',
                str(status.created_at),
                status.text
            )
            send_updates()

        def on_data(self, raw_data):
            print('Tuit received')
            json_data = json.loads(raw_data)
            tweet_time = datetime.datetime.strptime(json_data['created_at'], Twitter.ORIGINAL_TIME_FORMAT)

            StorageManager.save(
                'twitter',
                tweet_time.strftime(Twitter.FILENAME_TIME_FORMAT),
                json_data['text']
            )
            send_updates()

    def run(self):
        print('Twitter consumer running')
        auth = tweepy.OAuthHandler(Twitter.CONSUMER_KEY, Twitter.CONSUMER_SECRET)
        auth.set_access_token(Twitter.ACCESS_KEY, Twitter.ACCESS_SECRET)
        api = tweepy.API(auth)
        my_stream_listener = Twitter.MyStreamListener(api=api)
        my_stream = tweepy.streaming.Stream(auth=auth, listener=my_stream_listener)
        my_stream.filter(track=['soria'], locations=Twitter.CITY_LOCATIONS, languages=['es'])
