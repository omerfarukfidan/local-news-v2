import pyodbc
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add the root directory to sys.path to make sure 'app' is found
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)

try:
    from app.database import get_db_connection
except ModuleNotFoundError as e:
    print(f"Module import failed: {e}")

# Functions to create tables and populate the city table
def create_city_and_citynews_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create City table with unique identifiers for cities
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'City')
    BEGIN
        CREATE TABLE City (
            id INT PRIMARY KEY IDENTITY(1,1),
            city NVARCHAR(100) NOT NULL,
            state_id NVARCHAR(2) NULL,
            state_name NVARCHAR(100) NULL,
            lat DECIMAL(10, 6) NULL,
            lng DECIMAL(10, 6) NULL,
            population BIGINT NULL,
            zips NVARCHAR(MAX) NULL
        )
    END
    """)

    # Create CityNews table to handle many-to-many relationships between News and City
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CityNews')
    BEGIN
        CREATE TABLE CityNews (
            city_id INT NOT NULL,
            news_id INT NOT NULL,
            PRIMARY KEY (city_id, news_id),
            FOREIGN KEY (city_id) REFERENCES City(id),
            FOREIGN KEY (news_id) REFERENCES News(id)
        )
    END
    """)

    conn.commit()
    conn.close()
    print("City and CityNews tables created successfully.")

def populate_city_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert data from Cities to City table
    try:
        cursor.execute("""
        INSERT INTO City (city, state_id, state_name, lat, lng, population, zips)
        SELECT DISTINCT city, state_id, state_name, lat, lng, population, zips
        FROM Cities
        """)
        conn.commit()
    except pyodbc.Error as e:
        print(f"SQL Error: {e}")
    finally:
        conn.close()
    print("City table populated successfully.")

# Create tables and populate the City table
if __name__ == "__main__":
    create_city_and_citynews_tables()
    populate_city_table()
