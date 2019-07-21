import os
import threading


class SocketIOClient:
    @staticmethod
    def emit_file_added():
        def run_client():
            print('Emitting files added')
            print('PORT: {}'.format(os.getenv('PORT')))
            from socketIO_client import SocketIO
            socketIO = SocketIO('localhost', os.getenv('PORT'))
            socketIO.emit('files added', broadcast=True)
            print('Emitted!')
            socketIO.disconnect()

        def run_client_port_80():
            print('Emitting files added (port 80)')
            from socketIO_client import SocketIO
            socketIO = SocketIO('localhost', os.getenv('PORT'))
            socketIO.emit('files added', broadcast=True)
            print('Emitted! (port 80)')
            socketIO.disconnect()

        thread = threading.Thread(target=run_client)
        thread.start()

        thread_test_80 = threading.Thread(target=run_client_port_80)
        thread_test_80.start()
