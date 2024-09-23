# Modsen_practice

This project is a web application that allows users to search for and manage documents using Elasticsearch and a PostgreSQL. It is designed for scenarios where efficient retrieval and management of large volumes of text data are required, such as in content management systems, blogs, or knowledge bases. The application utilizes the asynchronous framework aiohttp and provides a RESTful API for interacting with the data.

## Technologies Used
- SQLAlchemy: ORM for working with relational databases.
- PostgreSQL: A powerful, open-source relational database system known for its reliability and performance.
- Elasticsearch: A search engine for efficient document searching.
- aiohttp: Asynchronous web framework for creating HTTP services.
- Docker: Containerization for easy deployment of the application.

## How to run
1. Clone repo
```
git clone https://github.com/kapedalex/Modsen_practice.git
cd Modsen_practice
```
2. Rename example.env into .env and change variables into yours
3. Start the containers
```
docker-compose up -d
```
4. Wait about 1 minute for the services to start

## API:

Allows you to search for documents based on a text query.

http://localhost:3000/search?query={query}

Deletes the document with the specified ID.

http://localhost:3000/search?query={id}

## TODO:
1. Tests
2. Improve error handling
