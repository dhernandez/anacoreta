import json
import traceback

from flask_socketio import emit

from app import app, socketio
from flask import render_template, request

from app.sentiment import Sentiment
from app.trendings.Trendings import Trendings


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    emit('connection', {'data': 'Connected'})
    trendings = Trendings.get_trendings()
    emit('trendings', json.dumps(trendings))
    sentiment = Sentiment.get_sentiment()
    emit('sentiment', {'sentiment': sentiment})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on_error_default
def default_error_handler(e):
    print('ERROR')
    print(request.event["message"])
    print(request.event["args"])
    traceback.print_exception(e)
