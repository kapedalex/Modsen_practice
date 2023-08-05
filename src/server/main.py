import elasticsearch
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from config import Session, create_elasticsearch_connection, INDEX, PY_HOST, PY_PORT
from models import Post, Rubric, PostRubric


async def search_documents(request: web.Request) -> web.Response:
    """Search document by request in Elastic, find it in DB and return first 20"""
    query = request.query.get('query')
    if not query:
        return web.Response(text='Query parameter is missing.', status=400)

    e = create_elasticsearch_connection()
    payload = {
        "query": {
            "match": {
                "text": query
            }
        },
        "size": 20,
    }

    try:
        response = e.search(index=INDEX, body=payload)
    except elasticsearch.exceptions.NotFoundError as e:
        return web.Response(text=f"Error connecting to Elasticsearch: {e}")

    if response["hits"]["total"]["value"] > 0:
        hits = response["hits"]["hits"]
        doc_ids = [hit["_id"] for hit in hits]
        print(doc_ids)
        session = Session()
        try:
            query_result = session.query(Post.id, Post.text, Post.created_date). \
                select_from(Post). \
                where(Post.id.in_(doc_ids)). \
                distinct(). \
                order_by(Post.created_date.asc()).all()

            print(query_result)
            return web.Response(text=str(query_result))
        finally:
            session.close()
    else:
        return web.Response(text='Nothing found in Elasticsearch.', status=404)


async def delete_documents(request: web.Request) -> web.Response:
    """Delete doc by ID everywhere"""
    query = request.query.get('query')

    if not query:
        return web.Response(text='Query parameter is missing.', status=400)

    try:
        session = Session()
        try:
            post = session.query(Post).get(query)
            if post:
                session.delete(post)
                session.commit()

                e = create_elasticsearch_connection()
                e.delete(index=INDEX, id=query)

                return web.Response(text='Document deleted successfully.')
            else:
                return web.Response(text='Document not found.', status=404)

        finally:
            session.close()

    except Exception as e:
        return web.Response(text=f"Error: {e}")


def main():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    f = fernet.Fernet(fernet_key)
    setup(app, EncryptedCookieStorage(f))
    app.router.add_get('/search', search_documents)
    app.router.add_get('/delete', delete_documents)
    web.run_app(app, host=PY_HOST, port=PY_PORT)


if __name__ == "__main__":
    main()
