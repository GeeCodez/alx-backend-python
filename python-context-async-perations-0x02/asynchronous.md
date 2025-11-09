# Asynchronous Programming in Python (Async/Await & aiosqlite)

## Table of Contents
1. [Introduction](#introduction)  
2. [Why Asynchronous Programming?](#why-asynchronous-programming)  
3. [Key Concepts](#key-concepts)  
    - Coroutines  
    - Event Loop  
    - `async` and `await`  
    - Concurrency vs Parallelism  
4. [Python Tools & Libraries](#python-tools--libraries)  
    - `asyncio`  
    - `aiosqlite`  
5. [Basic Syntax & Usage](#basic-syntax--usage)  
6. [Using `aiosqlite` for Async Databases](#using-aiosqlite-for-async-databases)  
7. [Practical Examples](#practical-examples)  
    - Async Functions  
    - Concurrent Database Queries  
8. [Best Practices](#best-practices)  
9. [Real-World Applications](#real-world-applications)  
10. [Conclusion](#conclusion)  

---

## Introduction

Asynchronous programming allows a program to **perform multiple tasks concurrently** without waiting for each task to complete sequentially.  
It is especially useful for **I/O-bound operations**, like database queries, network requests, or file operations.  

Using Python's `async`/`await` syntax, developers can write clean, readable, and high-performance code that **doesn’t block the program while waiting for slow operations**.

---

## Why Asynchronous Programming?

- Traditional synchronous programs run tasks **one after another**.  
- I/O operations block the program until completion.  

Example:

```python
import time

def download_file():
    # Blocks for 3 seconds
    time.sleep(3)
Multiple such operations make the program slow.

Async programming solves this by:

Allowing other tasks to run while waiting for I/O

Making programs more efficient and responsive

Reducing total execution time when multiple independent tasks are present

Key Concepts
1. Coroutines
Any function/task defined with async def

Can pause and resume using await

Example:

python
Copy code
import asyncio

async def fetch_data():
    await asyncio.sleep(2)
    return "Data fetched"

2. Event Loop
The engine that runs coroutines in Python

Manages which coroutine runs next while others are paused

Started using asyncio.run(main())

3. async and await
async def → declares a coroutine

await → pauses the coroutine until the awaited operation completes

4. Concurrency vs Parallelism
Term	        Meaning	Example
Concurrency	    Tasks take turns and appear simultaneous	Async database queries
Parallelism	    Tasks run truly at the same time on multiple CPU cores	Multi-threading / multi-processing

Python Tools & Libraries
asyncio
Python’s built-in async framework

Provides:

Event loop management

Running multiple coroutines concurrently

Utilities like asyncio.gather

aiosqlite
Async-compatible library for SQLite

Allows non-blocking database operations

Key functions:

async with aiosqlite.connect("db") → async connection

await cursor.fetchall() → fetch results asynchronously

Basic Syntax & Usage
Async Functions
python

async def greet():
    print("Hello")
    await asyncio.sleep(1)
    print("Goodbye")

Awaiting Results

result = await some_async_function()
Using asyncio.gather
python

await asyncio.gather(
    greet(),
    greet(),
    greet()
)
Runs multiple independent tasks concurrently

Returns results in the order tasks were passed

Using aiosqlite for Async Databases
Connecting to a Database

import aiosqlite
import asyncio

async def connect_db():
    async with aiosqlite.connect("mydb.db") as db:
        # Connection automatically closes
        pass

asyncio.run(connect_db())
Using Cursors

async with db.execute("SELECT * FROM users") as cursor:
    rows = await cursor.fetchall()
cursor holds query state and methods for fetching

async with ensures it closes automatically

Inserting Data

await db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
await db.commit()

Multiple Rows

users = [("Alice", 25), ("Bob", 30)]
await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
await db.commit()
Practical Examples
Example 1: Async Functions

import asyncio

async def boil_water():
    print("Boiling water...")
    await asyncio.sleep(2)
    print("Water is ready!")

async def fry_egg():
    print("Frying egg...")
    await asyncio.sleep(3)
    print("Egg is done!")

async def main():
    await asyncio.gather(
        boil_water(),
        fry_egg()
    )

asyncio.run(main())
Example 2: Concurrent Database Queries

import asyncio
import aiosqlite

async def fetch_all_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def main():
    all_users, older_users = await asyncio.gather(
        fetch_all_users(),
        fetch_older_users()
    )
    
    print("All users:")
    for user in all_users:
        print(user)
        
    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

asyncio.run(main())
Best Practices
Use async with for connections/cursors — automatically closes resources

Use await only inside async def functions

Use asyncio.gather() for independent tasks, not sequential dependencies

Avoid blocking calls like time.sleep() — use await asyncio.sleep()

Keep async functions modular for easier concurrent execution

Real-World Applications
Web Servers: FastAPI, aiohttp — handle thousands of requests concurrently

Database Operations: Run multiple queries concurrently for analytics

APIs: Fetch data from multiple external APIs at the same time

File/Network I/O: Efficiently process large files or streams

Conclusion
Asynchronous programming in Python:

Makes I/O-heavy programs efficient and responsive

Enables multiple independent tasks to run concurrently

Works seamlessly with async libraries like aiosqlite

Essential for modern backend development, data pipelines, and web applications

By mastering async/await, asyncio.gather, and async database operations, you can build high-performance Python applications that scale efficiently.