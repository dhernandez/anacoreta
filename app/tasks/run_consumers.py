#!/usr/bin/python
from dotenv import load_dotenv

from app.consumers.Twitter import Twitter
from app.consumers.Newspapers import Newspaper


def run_consumers():
    run_twitter_consumer()
    run_newspaper_consumer()


def run_twitter_consumer():
    twitter = Twitter()
    twitter.start()


def run_newspaper_consumer():
    newspaper = Newspaper()
    newspaper.start()


if __name__ == '__main__':
    load_dotenv()
    run_consumers()
