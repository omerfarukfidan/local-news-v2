import sys
import os
import pandas as pd
import pyodbc

# Dynamically set the path to the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add the root directory to sys.path to allow importing app.database
sys.path.append(root_dir)

# Import the database connection function
from app.database import get_db_connection

# Load the cleaned CSV file from the dataset directory
csv_file_path = os.path.join(root_dir, 'dataset/cleaned_uscities.csv')
df = pd.read_csv(csv_file_path)

# Verify if data is loaded correctly
print(f"Loaded {len(df)} rows from cleaned_uscities.csv")

# Check the first few rows of the DataFrame
print(df.head())

# Convert columns to numeric where needed, coercing errors to NaN, and fill NaN with default value (e.g., 0.0)
df['lat'] = pd.to_numeric(df['lat'], errors='coerce').fillna(0.0).round(6)
df['lng'] = pd.to_numeric(df['lng'], errors='coerce').fillna(0.0).round(6)
df['population'] = pd.to_numeric(df['population'], errors='coerce').fillna(0)

# Fill missing zips with an empty string
df['zips'] = df['zips'].fillna('')

# Connect to SQL Server
conn = get_db_connection()
cursor = conn.cursor()

# Insert each row from the DataFrame into the SQL Server table
for index, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO Cities (city, city_ascii, state_id, state_name, lat, lng, population, zips)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, row['city'], row['city_ascii'], row['state_id'], row['state_name'], 
            row['lat'], row['lng'], row['population'], row['zips'])
    except pyodbc.Error as e:
        print(f"Error inserting row {index}: {e}")
        print(f"Row data: {row}")

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Data insertion completed successfully!")
