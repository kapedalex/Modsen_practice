"""
Config for DRY
"""
import sys

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


def create_postgres_connection(pg_db_name: str = PG_DB_NAME, pg_user: str = PG_USER, pg_host: str = PG_HOST
                               , pg_pass: str = PG_PASS, pg_port: str = PG_PORT):
    """Create postgres connection"""
    try:
        return psycopg2.connect(
            f"dbname='{pg_db_name}' user='{pg_user}' host='{pg_host}' password='{pg_pass}' port='{pg_port}'"
        )
    except psycopg2.Error as e:
        raise psycopg2.Error(f"Error connecting to Postgres: {e}")


def create_elasticsearch_connection(es_url: str = ES_URL):
    """Create es connection"""
    try:
        return Elasticsearch(es_url)
    except elasticsearch.exceptions.NotFoundError as e:
        raise elasticsearch.exceptions.NotFoundError(f"Error connecting to Elasticsearch: {e}")


# class ExecutePGquery:
#     def __init__(self):
#         self.conn = create_postgres_connection()
#         self.cur = self.conn.cursor()
#
#     def __enter__(self):
#         return self.cur
#
#     def __exit__(self, type, value, traceback):
#         self.conn.commit()
#         self.cur.close()
#         self.conn.close()


class PGQueryExecutor:
    conn = create_postgres_connection()
    cur = conn.cursor()

    @classmethod
    def execute(cls, query, *args):
        cls.cur.execute(query, *args)
        cls.conn.commit()

    @classmethod
    def close(cls):
        cls.cur.close()
        cls.conn.close()
