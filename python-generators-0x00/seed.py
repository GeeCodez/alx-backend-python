import os
import csv
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection info from .env
DB_NAME = os.getenv("PG_DB", "alx_prodev")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")

def connect_db():
    """Connect to the PostgreSQL server (admin connection)."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # default admin db
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def create_database(connection):
    """Create database ALX_prodev if it doesn't exist."""
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'alx_prodev';")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE alx_prodev;")
        print("Database ALX_prodev created successfully")
    cursor.close()

def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create table user_data if it doesn’t exist."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id UUID PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    """Insert data into user_data table from CSV file."""
    cursor = connection.cursor()
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING;
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    print("Data inserted successfully")
    cursor.close()
