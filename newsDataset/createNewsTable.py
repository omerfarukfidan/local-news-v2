import sys
import os
import pandas as pd
import pyodbc

# Add the root project directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from app.database import get_db_connection

# Load the CSV file containing the combined news articles
csv_path = r"C:\Users\omerf\Documents\LocalNews\LocalNews\newsDataset\combined_news_articles.csv"
df = pd.read_csv(csv_path)

# Replace NaN with an empty string
df = df.fillna('')

# Convert all data to strings to avoid type mismatch issues
df['title'] = df['title'].astype(str)
df['content'] = df['content'].astype(str)
df['url'] = df['url'].astype(str)

# Get database connection
conn = get_db_connection()
cursor = conn.cursor()

# SQL command to create a table named 'News' if it doesn't exist
create_table_query = """
IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME = 'News'
)
BEGIN
    CREATE TABLE News (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(MAX),
        content NVARCHAR(MAX),
        url NVARCHAR(2083)
    )
END
"""

# Execute the create table command
cursor.execute(create_table_query)
conn.commit()

# Insert data from DataFrame to the database
insert_query = """
INSERT INTO News (title, content, url)
VALUES (?, ?, ?)
"""

# Iterate over the DataFrame and insert each row into the database
for _, row in df.iterrows():
    try:
        cursor.execute(insert_query, row['title'], row['content'], row['url'])
    except pyodbc.Error as e:
        print(f"Error inserting row: {e}, Title: {row['title']}")

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data successfully inserted into the 'News' table.")
