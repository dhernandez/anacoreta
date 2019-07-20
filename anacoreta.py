import os

from app import app, socketio

socketio.run(app, port=os.getenv('PORT'))
