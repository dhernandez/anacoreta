web: gunicorn -k gevent -w 1 anacoreta:app
release: python scripts/create_postgresql_table.py
worker: python -m app.tasks.run_consumers
