import os
import threading
import newspaper

from datetime import timedelta
from timeloop import Timeloop
from app.client.SocketIOClient import SocketIOClient
from app.storage.StorageManager import StorageManager


class Newspaper(threading.Thread):

    SOURCES = {
        'sorianoticias': 'http://sorianoticias.com',
        'elmiron': 'https://elmirondesoria.es',
        'desdesoria': 'http://www.desdesoria.es',
        'heraldodiariodesoria': 'http://www.heraldodiariodesoria.es',
    }

    running = False
    tl = Timeloop()

    def __init__(self):
        threading.Thread.__init__(self)

        @self.tl.job(interval=timedelta(minutes=float(os.getenv('CHECK_NEWS_LAPSE_IN_MINUTES'))))
        def check_news():
            print('Periodic search for news')
            if self.running:
                print('Last call is running yet')
                return
            self.running = True
            self.get_new_articles()
            self.running = False

    def run(self):
        print('Newspaper consumer running')
        self.tl.start()

    def get_new_articles(self):
        for key, source in self.SOURCES.items():
            paper = newspaper.build(source, language='es', memoize_articles=True)
            for article in paper.articles:
                try:
                    article.download()
                    article.parse()
                    StorageManager.save(
                        key,
                        article.publish_date,
                        '{} \n {}'.format(article.title, article.text)
                    )
                    SocketIOClient.emit_file_added()
                except:
                    pass
