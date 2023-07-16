"""
Config for DRY
"""
import contextlib
import elasticsearch
import psycopg2
from elasticsearch import Elasticsearch
from typing import Any
import os

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


@contextlib.contextmanager
def execute_pg_query(query: str, fetch: str = "all", params=None) -> Any:
    """Simple postgres queries use. I wonder if I did it wrong?"""

    conn = create_postgres_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, params)
        conn.commit()
        result = None

        if fetch == "all":
            result = cur.fetchall()
        elif fetch == "one":
            result = cur.fetchone()

        yield result
    finally:
        cur.close()
        conn.close()