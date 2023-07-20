"""
Config for DRY
"""
import elasticsearch
from elasticsearch import Elasticsearch
import os
import psycopg2

ES_URL = os.environ.get('ELASTIC_URL')
PG_DB_NAME = os.environ.get('POSTGRES_DB')
PG_USER = os.environ.get('POSTGRES_USER')
PG_PASS = os.environ.get('POSTGRES_PASSWORD')
PG_HOST = os.environ.get('POSTGRES_HOST')
PG_PORT = os.environ.get('POSTGRES_PORT')
PY_PORT = os.environ.get('PYTHON_PORT')
PY_HOST = os.environ.get('APP_HOST')
INDEX = "posts"


def create_postgres_connection():
    """Create postgres connection"""
    try:
        return psycopg2.connect(
            f"dbname='{PG_DB_NAME}' user='{PG_USER}' host='{PG_HOST}' password='{PG_PASS}' port='{PG_PORT}'"
        )
    except psycopg2.Error as e:
        raise psycopg2.Error(f"Error connecting to Postgres: {e}")


def create_elasticsearch_connection():
    """Create es connection"""
    try:
        return Elasticsearch(ES_URL)
    except elasticsearch.exceptions.NotFoundError as e:
        raise elasticsearch.exceptions.NotFoundError(f"Error connecting to Elasticsearch: {e}")


class ExecutePGquery:
    def __init__(self):
        self.conn = create_postgres_connection()
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
