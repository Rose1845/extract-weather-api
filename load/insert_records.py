
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
        city        TEXT,
        country     TEXT,
        timestamp   TIMESTAMP,
        temperature FLOAT,
        feels_like  FLOAT,
        humidity    INT,
        pressure    INT,
        wind_speed  FLOAT,
        weather     TEXT,
        description TEXT,
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


def insert_weather_data():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather (city, country, timestamp, temperature, feels_like,
                             humidity, pressure, wind_speed, weather, description)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """)
    conn.commit()
    conn.close()
