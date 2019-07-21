#!/usr/bin/python
import os

from dotenv import load_dotenv


def run_consumers():
    run_twitter_consumer()


def run_twitter_consumer():
    from app.consumers.Twitter import Twitter
    twitter = Twitter()
    twitter.start()


def run_newspaper_consumer():
    from app.consumers.Newspapers import Newspaper
    newspaper = Newspaper()
    newspaper.start()


if __name__ == '__main__':
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app/.env'))
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env'))
    run_consumers()
