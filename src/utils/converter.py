"""
Скрипт для ввода данных в postgres и elasticsearch с исходного csv
"""

import csv
import os
import sys
import pandas as pd
import psycopg2

# TODO: fix sys.path problem
sys.path.append('.')
from server import config


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
    try:
        conn = config.create_postgres_connection()
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS posts;")
        cur.execute("""CREATE TABLE posts(
            id SERIAL PRIMARY KEY,
            text text NOT NULL,
            created_date date NOT NULL
        )
        """)

        cur.execute("DROP TABLE IF EXISTS rubrics;")
        cur.execute("""CREATE TABLE rubrics(
            id SERIAL PRIMARY KEY,
            rubric text NOT NULL
        )
        """)

        cur.execute("DROP TABLE IF EXISTS post_rubrics;")
        cur.execute("""CREATE TABLE post_rubrics(
            post_id INT REFERENCES posts(id),
            rubric_id INT REFERENCES rubrics(id),
            PRIMARY KEY (post_id, rubric_id)
        )
        """)

        # TODO: bulk. I know it is worse than was.
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                sql = "INSERT INTO posts (text, created_date) VALUES (%s, %s) RETURNING id;"
                cur.execute(sql, (row[0], row[1]))
                post_id = cur.fetchone()[0]

                rubrics = eval(row[2])
                for rubric in rubrics:
                    sql = "INSERT INTO rubrics (rubric) VALUES (%s) RETURNING id;"
                    cur.execute(sql, (rubric,))
                    rubric_id = cur.fetchone()[0]

                    sql = "INSERT INTO post_rubrics (post_id, rubric_id) VALUES (%s, %s);"
                    cur.execute(sql, (post_id, rubric_id))

        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error connecting to Postgres converter: {e}")


def main():
    file_name = "./posts.csv"
    postgres_insert_logic(file_name)
    elastic_insert_logic(file_name)


if __name__ == "__main__":
    os.chdir('utils')
    main()
    os.chdir('../')
