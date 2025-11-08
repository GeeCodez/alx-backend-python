import sqlite3
import functools
import csv

# -------------------------
# Decorator for handling connections safely
# -------------------------
def with_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            try:
                result = func(conn, *args, **kwargs)
                conn.commit()
                return result
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
            except Exception as e:
                print(f"Unexpected error: {e}")
                conn.rollback()
    return wrapper


# -------------------------
# Create table if it doesn't exist
# -------------------------
@with_connection
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        );
    """)
    print("✅ Table created successfully.")

# @with_connection
# def manual_data_insert(conn,name,email,age):
#     cursor=conn.cursor()
#     query="""INSERT INTO users(name,email,age)
#     VALUES (?,?,?)
#     """
#     cursor.execute(query,(name,email,age))
#     print(f"{name} inserted succesfully")

# -------------------------
# Generator to stream rows from CSV file
# -------------------------
def stream_csv_rows(csv_file):
    """Yields rows from CSV one by one as tuples."""
    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip incomplete rows
                if not all([row.get('name'), row.get('email'), row.get('age')]):
                    continue
                yield (row['name'], row['email'], int(row['age']))
    except FileNotFoundError:
        print(f"❌ File '{csv_file}' not found.")
    except KeyError as e:
        print(f"❌ Missing column in CSV: {e}")


# -------------------------
# Insert generator data in batches
# -------------------------
@with_connection
def insert_from_generator(conn, csv_file, batch_size=500):
    cursor = conn.cursor()
    batch = []
    total_inserted = 0

    for row in stream_csv_rows(csv_file):
        batch.append(row)

        # Once batch is full, insert it
        if len(batch) == batch_size:
            cursor.executemany("""
                INSERT OR IGNORE INTO users (name, email, age)
                VALUES (?, ?, ?)
            """, batch)
            total_inserted += cursor.rowcount
            batch.clear()  # clear the list to reuse memory

    # Insert remaining rows (if any)
    if batch:
        cursor.executemany("""
            INSERT OR IGNORE INTO users (name, email, age)
            VALUES (?, ?, ?)
        """, batch)
        total_inserted += cursor.rowcount

    print(f"✅ Inserted {total_inserted} records from {csv_file} in batches of {batch_size}.")


# -------------------------
# Main driver
# -------------------------
def main():
    create_table()
    insert_from_generator("python-generators-0x00/user_data.csv", batch_size=500)


if __name__ == "__main__":
    main()