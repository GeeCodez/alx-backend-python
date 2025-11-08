import sqlite3
import functools

class DatabaseConnection:
    """creating a customer class based context manager for handling database connection"""
    def __init__(self,dbname):
        self.dbname=dbname
        self.conn=None
    
    def __enter__(self):
        self.conn=sqlite3.connect(self.dbname)
        print(f"Database {self.dbname} connected")
        return self.conn
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.conn:
            self.conn.close()
            print("database closed")

def with_connection(func):
    functools.wraps(func)
    def wrapper(*args,**kwargs):
        with DatabaseConnection("users.db") as conn:
            return func(conn,*args,**kwargs)
    return wrapper

@with_connection
def fetch_usernames(conn):
    cursor=conn.cursor()
    cursor.execute("SELECT name from users WHERE age<18 LIMIT 10")
    return cursor.fetchall()

for i in fetch_usernames():
    print(i)

    
# with DatabaseConnection("users.db") as conn:
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM users LIMIT 10")
#     result=cursor.fetchall()
#     for i in result: print(str(i))