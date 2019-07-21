import datetime
import os
import traceback
import uuid

import psycopg2
import psycopg2.extras


class PostgreSQL:
    @staticmethod
    def _get_postgresql_connection():
        psycopg2.extras.register_uuid()
        PostgreSQL.connection = None
        database_url = os.environ['DATABASE_URL']
        return psycopg2.connect(database_url, sslmode='require')

    @staticmethod
    def save(source, date, text):
        with PostgreSQL._get_postgresql_connection() as conn:
            with conn.cursor() as cur:
                sql = 'INSERT INTO sources (id, source, publish_date, content) VALUES (%s, %s, %s, %s)'
                data = (uuid.uuid4(), source, date, text,)
                cur.execute(sql, data)
                conn.commit()

    @staticmethod
    def get_last_texts(minutes):
        now = datetime.datetime.now()
        trendings_from = now - datetime.timedelta(minutes=minutes)

        with PostgreSQL._get_postgresql_connection() as conn:
            with conn.cursor() as cur:
                sql = 'SELECT content FROM sources WHERE publish_date > %s'
                data = (trendings_from,)
                cur.execute(sql, data)
                recent_text = [result[0] for result in cur.fetchall()]

        return recent_text
