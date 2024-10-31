import psycopg2
import json
import sys
import os

# Get the current directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to your config.json file
config_path = os.path.join(current_dir, 'config.json')

# Load the JSON config file
with open(config_path) as config_file:
    config = json.load(config_file)

def get_db_connection():
    # Fetching the connection details from JSON config
    server = config['DB_SERVER']
    port = config['DB_PORT']
    database = config['DB_NAME']
    user = config['DB_USER']
    password = config['DB_PASSWORD']
    sslmode = config['DB_SSL_MODE']

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=server,
            port=port,
            dbname=database,
            user=user,
            password=password,
            sslmode=sslmode
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

# Test the function
get_db_connection()
