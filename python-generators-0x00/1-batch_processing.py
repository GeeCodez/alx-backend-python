#!/usr/bin/python3
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection setup
def get_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        database=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        port=os.getenv("PG_PORT", 5432)
    )


# Generator: fetch users in batches
def stream_users_in_batches(batch_size):
    """
    Yields user records from the users table in batches of batch_size.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, email, age FROM user_data;")

    while True:
        rows = cur.fetchmany(batch_size)
        if not rows:
            break
        yield [
            {"user_id": r[0], "name": r[1], "email": r[2], "age": r[3]}
            for r in rows
        ]

    cur.close()
    conn.close()


# Process batches: filter users over 25
def batch_processing(batch_size):
    """
    Processes each batch of users and prints only those older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
