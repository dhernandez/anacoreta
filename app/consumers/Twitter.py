import datetime
import json
import os
import threading

import tweepy

from app import socketio
from app.client.SocketIOClient import SocketIOClient
from app.storage.StorageManager import StorageManager


class Twitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.DIRECTORY = os.getenv('SOURCES_DIRECTORY')
        self.CONSUMER_KEY = os.getenv('CONSUMER_KEY')
        self.CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
        self.ACCESS_KEY = os.getenv('ACCESS_KEY')
        self.ACCESS_SECRET = os.getenv('ACCESS_SECRET')
        self.FILENAME_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.ORIGINAL_TIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'
        self.CITY_LOCATIONS = [-3.3723, 41.2785, -1.999, 42.001]


    class MyStreamListener(tweepy.streaming.StreamListener):
        def on_status(self, status):
            StorageManager.save(
                'twitter',
                str(status.created_at),
                status.text
            )
            socketio.emit('files added', broadcast=True)
            SocketIOClient.emit_file_added()

        def on_data(self, raw_data):
            json_data = json.loads(raw_data)
            tweet_time = datetime.datetime.strptime(json_data['created_at'], Twitter.ORIGINAL_TIME_FORMAT)

            StorageManager.save(
                'twitter',
                tweet_time.strftime(Twitter.FILENAME_TIME_FORMAT),
                json_data['text']
            )
            SocketIOClient.emit_file_added()

    def run(self):
        print('Authenticating...')
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        api = tweepy.API(auth)
        print('Authenticated')
        my_stream_listener = self.MyStreamListener(api=api)
        my_stream = tweepy.streaming.Stream(auth=auth, listener=my_stream_listener)
        my_stream.filter(locations=self.CITY_LOCATIONS, languages=['es'])
