#!/usr/bin/python
import os
import argparse
import sys

from dotenv import load_dotenv


def process_arguments():
    parser = argparse.ArgumentParser(description='Consuming some sources.')
    parser.add_argument(
        '-s',
        '--sources',
        choices=['twitter', 'newspaper'],
        type=str, nargs='+',
        required=True,
    )
    return parser.parse_args()


def run_twitter_consumer():
    from app.consumers.Twitter import Twitter
    twitter = Twitter()
    twitter.start()
    return twitter


def run_newspaper_consumer():
    from app.consumers.Newspaper import Newspaper
    newspaper = Newspaper()
    newspaper.start()
    return newspaper


if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env'))
    args = process_arguments()
    consumer_threads = []
    for source in args.sources:
        source_consumer = 'run_{}_consumer'.format(source)
        source_consumer_callable = getattr(sys.modules[__name__], source_consumer)
        consumer_threads.append(source_consumer_callable())
    for consumer in consumer_threads:
        consumer.join()
