import asyncio
import aiosqlite
import time

async def fetch_all_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM USERS LIMIT 20") as cursor:
            result=await cursor.fetchall()
            print("All users in database")
            for row in result:
                print(row)

async def fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age>40 LIMIT 20") as cursor:
            rows=await cursor.fetchall()
            print("\n Older users")
            for row in rows:
                print(row)

async def fetch_concurrently():
    await asyncio.gather(
        fetch_all_users(),
        fetch_older_users()
    )
start=time.time()
asyncio.run(fetch_concurrently())
end=time.time()
print(f"Query executed within {end-start:.2f} seconds")
