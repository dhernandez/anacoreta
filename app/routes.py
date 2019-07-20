import traceback

from flask_socketio import emit

from app import app, socketio
from flask import render_template, request


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on_error_default
def default_error_handler(e):
    print('ERROR')
    print(request.event["message"])
    print(request.event["args"])
    traceback.print_exception(e)
