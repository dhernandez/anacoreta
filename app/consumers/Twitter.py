import datetime
import json
import os
import threading

import tweepy

from app import socketio
from app.client.SocketIOClient import SocketIOClient
from app.storage.StorageManager import StorageManager


class Twitter(threading.Thread):
    DIRECTORY = os.getenv('SOURCES_DIRECTORY')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    ACCESS_SECRET = os.getenv('ACCESS_SECRET')
    FILENAME_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    ORIGINAL_TIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'
    CITY_LOCATIONS = os.getenv('CITY_LOCATION').split(',')

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
        auth = tweepy.OAuthHandler(Twitter.CONSUMER_KEY, Twitter.CONSUMER_SECRET)
        auth.set_access_token(Twitter.ACCESS_KEY, Twitter.ACCESS_SECRET)
        api = tweepy.API(auth)
        my_stream_listener = Twitter.MyStreamListener(api=api)
        my_stream = tweepy.streaming.Stream(auth=auth, listener=my_stream_listener)
        my_stream.filter(locations=Twitter.CITY_LOCATIONS, languages=['es'])
