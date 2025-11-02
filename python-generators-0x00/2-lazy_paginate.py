#!/usr/bin/python3
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DB_NAME = os.getenv("PG_DB")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")


def paginate_users(page_size, offset):
    """Fetch a single page of users from the database."""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (page_size, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads paginated data from the users table.
    Uses only one loop and yields one page at a time.
    """
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size
