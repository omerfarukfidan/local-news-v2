import sys
import os
import pyodbc

# Add the root folder to sys.path (in case you are working in a subfolder)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the database connection function
from app.database import get_db_connection

# Connect to SQL Server
conn = get_db_connection()
cursor = conn.cursor()

# Insert a single test row into the Cities table
try:
    cursor.execute("""
        INSERT INTO Cities (city, city_ascii, state_id, state_name, lat, lng, population, density, zips)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 'Test City', 'Test City', 'TS', 'Test State', 45.123456, -93.123456, 1000000, 1234.56, '12345')

    # Commit the transaction
    conn.commit()
    print("Test row successfully inserted into Cities table.")
except pyodbc.Error as e:
    print(f"Error inserting test row: {e}")

# Close the connection
conn.close()
