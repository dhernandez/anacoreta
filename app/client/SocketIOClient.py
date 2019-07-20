import threading


class SocketIOClient:
    @staticmethod
    def emit_file_added():
        def run_client():
            from socketIO_client import SocketIO, LoggingNamespace
            socketIO = SocketIO('localhost', 5000, LoggingNamespace)
            socketIO.emit('files added', broadcast=True)
            socketIO.disconnect()

        thread = threading.Thread(target=run_client)
        thread.start()
