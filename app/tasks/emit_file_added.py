#!/usr/bin/python
import os

from dotenv import load_dotenv

from app.client.SocketIOClient import SocketIOClient

if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env'))
    SocketIOClient.emit_file_added()
