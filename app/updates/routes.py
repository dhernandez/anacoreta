import json

from app.sentiment import Sentiment
from app.trendings.Trendings import Trendings

from .. import socketio


@socketio.on('files added')
def send_updated_data():
    trendings = Trendings.get_trendings()
    socketio.emit('trendings', json.dumps(trendings))
    sentiment = Sentiment.get_sentiment()
    socketio.emit('sentiment', {'sentiment': sentiment})
