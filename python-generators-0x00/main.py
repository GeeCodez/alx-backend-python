#!/usr/bin/python3
"""0-main.py: Test script for seed.py"""

# Import your seed module
seed = __import__('seed')

# Step 1: Connect to the PostgreSQL server
connection = seed.connect_db()
if connection:
    # Step 2: Create database (if it doesn’t exist)
    seed.create_database(connection)
    connection.close()
    print("✅ connection successful")

    # Step 3: Connect to the new database
    connection = seed.connect_to_prodev()

    if connection:
        # Step 4: Create the user_data table
        seed.create_table(connection)

        # Step 5: Insert CSV data
        seed.insert_data(connection, 'python-generators-0x00/user_data.csv')

        # Step 6: Verify database and print 5 rows
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'alx_prodev';")
        result = cursor.fetchone()
        if result:
            print("✅ Database alx_prodev is present")

        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print("\n📊 Sample Data:")
        for row in rows:
            print(row)
        cursor.close()
