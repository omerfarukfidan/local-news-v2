import psycopg2
import os
import sys

from app import load_config 

def get_db_connection():
    config = load_config()  
    
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=config["DB_SERVER"],
            port=config["DB_PORT"],
            dbname=config["DB_NAME"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            sslmode=config["DB_SSL_MODE"]
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
