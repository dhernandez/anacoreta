import json
import os

from dotenv import load_dotenv
from flask_socketio import SocketIO

from app.sentiment import Sentiment
from app.trendings.Trendings import Trendings


def send_updates():
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env'))
    redis_url = os.getenv('REDISTOGO_URL', 'redis://')
    socketio = SocketIO(message_queue=redis_url)
    trendings = Trendings.get_trendings()
    socketio.emit('trendings', json.dumps(trendings))
    sentiment = Sentiment.get_sentiment()
    socketio.emit('sentiment', {'sentiment': sentiment})


if __name__ == '__main__':
    send_updates()
