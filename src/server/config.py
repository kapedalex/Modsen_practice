import os

from elasticsearch import Elasticsearch
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import elasticsearch

INDEX = os.environ.get('INDEX')
PY_PORT = os.environ.get('PYTHON_PORT')
PY_HOST = os.environ.get('APP_HOST')
ES_URL = os.environ.get('ELASTIC_URL')
DB_URL = os.environ.get('DB_URL')

engine = create_engine(DB_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_elasticsearch_connection(es_url: str = ES_URL):
    """Create es connection"""
    try:
        return Elasticsearch(es_url)
    except elasticsearch.exceptions.NotFoundError as e:
        raise elasticsearch.exceptions.NotFoundError(f"Error connecting to Elasticsearch: {e}")