# Modsen_practice

Used:
- psycopg2
- elasticsearch
- aiohttp

# How to run
1. Clone repo
2. Rename example.env into .env and change variables into yours
2. docker-compose up -d
3. Wait for 1 minute


Requests in format:

http://localhost:3000/search?query={query}

http://localhost:3000/search?query={id}

# TODO:
1. Bulk
2. Tests
3. ..?