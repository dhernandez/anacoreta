#!/usr/bin/python


def run_consumers():
    run_twitter_consumer()
    run_newspaper_consumer()


def run_twitter_consumer():
    from app.consumers.Twitter import Twitter
    twitter = Twitter()
    twitter.start()


def run_newspaper_consumer():
    from app.consumers.Newspapers import Newspaper
    newspaper = Newspaper()
    newspaper.start()


if __name__ == '__main__':
    run_consumers()
