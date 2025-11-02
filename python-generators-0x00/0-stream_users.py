import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def stream_users():
    """Generator that yields users one by one from the database."""
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB", "alx_prodev"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5432"),
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield dict(row)
    cursor.close()
    conn.close()
