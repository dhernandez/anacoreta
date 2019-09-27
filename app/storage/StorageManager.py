import importlib
import os


class StorageManager:
    FILES = 'files'
    POSTGRESQL = 'postgresql'

    @staticmethod
    def save(source, date, text):
        return StorageManager._get_strategy(os.getenv('STORAGE')).save(source, date, text)

    @staticmethod
    def get_last_texts(minutes):
        return StorageManager._get_strategy(os.getenv('STORAGE')).get_last_texts(minutes)

    @staticmethod
    def _get_strategy(strategy):
        switcher = {
            StorageManager.FILES: 'Files',
            StorageManager.POSTGRESQL: 'PostgreSQL'
        }

        class_name = switcher.get(strategy, 'Files')
        return getattr(importlib.import_module('app.storage.strategy.{}'.format(class_name)), class_name)
