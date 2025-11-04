import time 
import sqlite3
import functools

def with_db_connection(db_name='users.db'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            conn=sqlite3.connect(db_name)
            try:
                return func(conn,*args,**kwargs)
            except Exception as e:
                print(f"Error executing query: {e}")
            finally:
                conn.close()
        return wrapper
    return decorator

#creating the function that makes the retry
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print("All retry attempts failed. Raising exception.")
                        raise
                    else:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection()
@retry_on_failure(retries=3,delay=1)
def fetch_users_with_retry(conn):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM  users")
    return cursor.fetchall()
    ##attempting to fetch users with automatic retry on failure

users=fetch_users_with_retry()
print(users)