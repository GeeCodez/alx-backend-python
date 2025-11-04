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

@with_db_connection()
def get_user_by_id(conn,user_id):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?",(user_id,))
    return cursor.fetchone()
    ##fetch user by id with automatic connection handling

user=get_user_by_id(user_id=1)
print(user)