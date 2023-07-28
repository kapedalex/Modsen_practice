import csv
import os
import sys

import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# TODO: fix sys.path problem
sys.path.append('.')
from server.models import Post, Rubric, PostRubric, PostCreate
from server import config

Base = declarative_base()


def elastic_insert_logic(file_name: str):
    """Elastic data add"""
    df = pd.read_csv(file_name, usecols=[0])
    df["id"] = df.index + 1
    print(df)

    e = config.create_elasticsearch_connection()

    if e.indices.exists(index=config.INDEX):
        e.indices.delete(index=config.INDEX)
    e.indices.create(index=config.INDEX)

    for _, row in df.iterrows():
        document = row.to_dict()
        document_id = row['id']
        e.index(index=config.INDEX, id=document_id, body=document)


def postgres_insert_logic(file_name: str):
    """Postgres data add"""
    Session = sessionmaker(bind=config.engine)
    session = Session()

    try:
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                text, created_date, rubrics = row

                post_data = PostCreate(text=text, created_date=created_date, rubrics=eval(rubrics))

                post = Post(**post_data.dict(exclude={'rubrics'}))
                session.add(post)
                session.flush()

                for rubric_name in post_data.rubrics:
                    rubric = Rubric(rubric=rubric_name)
                    session.add(rubric)
                    session.flush()

                    post_rubric = PostRubric(post_id=post.id, rubric_id=rubric.id)
                    session.add(post_rubric)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting data into PostgreSQL: {e}")
    finally:
        session.close()


def main():
    file_name = "./posts.csv"
    postgres_insert_logic(file_name)
    elastic_insert_logic(file_name)


if __name__ == "__main__":
    os.chdir('utils')
    main()
    os.chdir('../')
