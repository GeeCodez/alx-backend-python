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

def transactional(func):
    """
    Decorator to automatically handle COMMIT and ROLLBACK
    for database transactions.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # ✅ Save changes if everything worked
            return result
        except Exception as e:
            conn.rollback()  # ❌ Undo changes if there was an error
            print(f"Transaction failed: {e}")
            raise  # Re-raise the error for debugging/logging
    return wrapper


@with_db_connection()
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')