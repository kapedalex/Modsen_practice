"""
Search and delete docs
"""
import psycopg2
import elasticsearch
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from src.server import config



async def search_documents(request: web.Request) -> web.Response:
    """Search document by request in Elastic, find it in DB and return first 20"""
    query = request.query.get('query')
    if not query:
        return web.Response(text='Query parameter is missing.', status=400)

    e = config.create_elasticsearch_connection()
    payload = {
        "query": {
            "match": {
                "text": query
            }
        },
        "size": 20,
    }

    try:
        response = e.search(index=config.INDEX, body=payload)
    except elasticsearch.exceptions.NotFoundError as e:
        return web.Response(text=f"Error connecting to Elasticsearch: {e}")

    if response["hits"]["total"]["value"] > 0:
        hits = response["hits"]["hits"]
        doc_ids = [hit["_id"] for hit in hits]

        with config.PGQueryExecutor() as executor:
            executor.execute("SELECT p.text, p.created_date, r.rubric FROM posts p "
                "JOIN post_rubrics pr ON p.id = pr.post_id "
                "JOIN rubrics r ON pr.rubric_id = r.id "
                "WHERE p.id::text = ANY(%s) ORDER BY p.created_date ASC;", [doc_ids])
            return web.Response(text=str(executor.fetchall()))

    else:
        return web.Response(text='Nothing found in Elasticsearch.', status=404)


async def delete_documents(request: web.Request) -> web.Response:
    """Delete doc by ID everywhere"""
    query = request.query.get('query')

    if not query:
        return web.Response(text='Query parameter is missing.', status=400)

    # There is strange CASCADE in postgres, so let it be simple
    try:
        with config.PGQueryExecutor() as executor:
            executor.execute("DELETE FROM post_rubrics WHERE post_id = %s;", [query])
            executor.execute("DELETE FROM posts WHERE id = %s;", [query])

        try:
            e = config.create_elasticsearch_connection()
            text = str(e.delete(index=config.INDEX, id=query))
            return web.Response(text=text)
        except elasticsearch.exceptions.NotFoundError as e:
            return web.Response(text=f"Error connecting to Elasticsearch: {e}")

    except psycopg2.Error as e:
        return web.Response(text=f"Error connecting to Postgres: {e}")


def main():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    f = fernet.Fernet(fernet_key)
    setup(app, EncryptedCookieStorage(f))
    app.router.add_get('/search', search_documents)
    app.router.add_get('/delete', delete_documents)
    web.run_app(app, host=config.PY_HOST, port=config.PY_PORT)


if __name__ == "__main__":
    main()
