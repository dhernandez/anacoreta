#!/usr/bin/python

import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app/.env'))

with psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require') as conn:
    with conn.cursor() as cur:
        sql = 'CREATE TABLE IF NOT EXISTS sources (id UUID PRIMARY KEY, source VARCHAR(50), publish_date TIMESTAMP, content TEXT)'
        cur.execute(sql)
        conn.commit()
