import os

import eventlet
from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO

from app.storage.StorageManager import StorageManager

load_dotenv()
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
redis_url = os.getenv('REDISTOGO_URL', 'redis://')
socketio = SocketIO(app, async_mode=async_mode, ping_interval=10, message_queue=redis_url)

from app import routes

eventlet.monkey_patch()
