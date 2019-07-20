import os

from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO

from app.storage.StorageManager import StorageManager


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


load_dotenv()

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

socketio = SocketIO(app, async_mode=async_mode)

from app.updates import bp as updates_bp
app.register_blueprint(updates_bp, )

from app import routes

run_consumers()
