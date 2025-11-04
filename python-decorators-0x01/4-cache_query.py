import time
import sqlite3
import functools

query_cache={}

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

def cache_query(func):
    """Caches SQL query results safely, handles all errors gracefully."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract SQL query and parameters
        q = kwargs.get('query') or (args[0] if args else None)
        params = kwargs.get('params') or (args[1] if len(args) > 1 else ())

        if not q:
            raise ValueError("No SQL query provided for caching.")

        # Create a cache key
        cache_key = (q, tuple(params))

        # If the query is already cached, return it
        if cache_key in query_cache:
            print(f"✅ In cache {cache_key}")
            return query_cache[cache_key]

        # If not cached, execute and cache it
        try:
            print(f"🔍 Executing query: {q} with params: {params}")
            results = func(conn, *args, **kwargs)
            query_cache[cache_key] = results
            print(f"💾 Cached result for {cache_key}")
            return results

        except Exception as e:
            print(f"⚠️ Error while executing query: {e}")
            return None
    return wrapper

@with_db_connection()
@cache_query
def fetch_users_with_cache(conn,query,params=None):
    cursor=conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#first call will cache the result
users=fetch_users_with_cache(query='SELECT * FROM users')

#second call will use the cached result
users_again=fetch_users_with_cache(query='SELECT * FROM users')