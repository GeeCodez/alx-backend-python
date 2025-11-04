import sqlite3
import functools

##decorator function to log queries 
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        q=kwargs.get('qeury') if 'query' in kwargs else (args[0] if len(args)>0 else None)
        #printing the query to the screen
        print(f"[LOG] function {func.__name__} executing SQL: {q}")
        #calling the original function
        return func(*args,**kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn=sqlite3.connect('users.db')
    cursor=conn.cursor()
    cursor.execute(query)
    results=cursor.fetchall()
    conn.close()
    return results

users=fetch_all_users(query="SELECT * from users")