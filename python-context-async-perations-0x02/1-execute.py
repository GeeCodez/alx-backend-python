import sqlite3

class ExecuteQuery:
    def __init__(self, query, dbname, params=()):
        self.query = query
        self.dbname = dbname
        self.params = params
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return False  # Let exceptions propagate if they occur


# ✅ Usage
query = "SELECT * FROM users WHERE age > ? LIMIT 10"
params = (25,)

with ExecuteQuery(query, "users.db", params) as results:
    for i in results:
        print(i)
