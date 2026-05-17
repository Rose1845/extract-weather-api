
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    """
    Connect to PostgreSQL using credentials from .env
    Returns a psycopg2 connection object
    """
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", 5432)
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    print("Connecting to PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        print("Connection successful!")
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed! {e}")
        return None


def create_weather_table():
    conn = connect_to_db()
    if conn is None:
        print("Cannot create table because connection failed.")
        return

    cur = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS weather (
        id BIGSERIAL PRIMARY KEY,
        city
        date TIMESTAMP,
        day_name TEXT,
        status TEXT,
        description TEXT,
        icon TEXT,
        temp_day FLOAT,
        temp_min FLOAT,
        temp_max FLOAT,
        temp_night FLOAT,
        humidity FLOAT
    );
    """
    try:
        cur.execute(create_table_query)
        conn.commit()
        print("Weather table created successfully!")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
    finally:
        cur.close()
        conn.close()


connect_to_db()
create_weather_table()


def insert_weather_data(day):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather (date, day_name, status, description, icon,
                             temp_day, temp_min, temp_max, temp_night, humidity)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        day["date"], day["day_name"], day["status"], day["description"],
        day["icon"], day["temp_day"], day["temp_min"], day["temp_max"],
        day["temp_night"], day["humidity"]
    ))
    conn.commit()
    conn.close()
