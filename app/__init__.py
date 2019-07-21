import os

from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO

from app.storage.StorageManager import StorageManager

load_dotenv()
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app, async_mode=async_mode)

from app.updates import bp as updates_bp
app.register_blueprint(updates_bp, )

from app import routes

