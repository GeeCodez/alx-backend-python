import asyncio
import aiosqlite
import time

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM USERS LIMIT 20") as cursor:
            result = await cursor.fetchall()
            return result

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age>40 LIMIT 20") as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    # Capture results from asyncio.gather
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users

# Measure execution time
start = time.time()
all_users, older_users = asyncio.run(fetch_concurrently())
end = time.time()

# Print results outside the functions
print("All users:")
for user in all_users:
    print(user)

print("\nUsers older than 40:")
for user in older_users:
    print(user)

print(f"\nQuery executed within {end-start:.2f} seconds")
