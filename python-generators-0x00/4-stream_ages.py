#!/usr/bin/python3
import seed  # reuse the connection logic from seed.py

def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")

    # Stream each row lazily
    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculates the average age of all users using the generator."""
    total_age = 0
    count = 0

    # One loop — consume the generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No user data found.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
