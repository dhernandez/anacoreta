#!/usr/bin/python
import os

from dotenv import load_dotenv


def run_consumers():
    return [run_twitter_consumer()]


def run_twitter_consumer():
    from app.consumers.Twitter import Twitter
    twitter = Twitter()
    twitter.start()
    return twitter


def run_newspaper_consumer():
    from app.consumers.Newspapers import Newspaper
    newspaper = Newspaper()
    newspaper.start()
    return newspaper


if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env'))
    consumers = run_consumers()
    for consumer in consumers:
        consumer.join()
