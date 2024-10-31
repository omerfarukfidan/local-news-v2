import openai
import os
import sys
from dotenv import load_dotenv
import random
import re

# Load environment variables
load_dotenv()

# Add the root directory to sys.path to make sure 'app' is found
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

try:
    from app.database import get_db_connection
except ModuleNotFoundError as e:
    print(f"Module import failed: {e}")
    sys.exit(1)

# Set up the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to normalize city names
def normalize_city_name(city_name):
    return re.sub(r'[^a-zA-Z\s]', '', city_name).strip().lower()

# Function to classify news by relevant American cities and assign to CityNews table
def classify_and_assign_news(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Select the first 'limit' unclassified news articles (using TOP for SQL Server)
    query = f"SELECT TOP {limit} id, title, content FROM News"
    cursor.execute(query)
    news_articles = cursor.fetchall()

    for article in news_articles:
        news_id, title, content = article

        # Prepare input for GPT-4 or fallback to GPT-3.5-turbo
        prompt = f"Identify the relevant American city or cities that this news article is related to.\nTitle: {title}\nContent: {content}\n"

        # Request city extraction from GPT model
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Change to "gpt-4" if available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that identifies cities from news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )

            # Extract response (assumes cities are listed one per line)
            output = response['choices'][0]['message']['content'].strip().split('\n')
            city_names = [normalize_city_name(city) for city in output if city.strip()]

            if city_names:
                for city_name in city_names:
                    print(f"Processing city: {city_name}")

                    # Fetch the city ID from the City table (ignoring case and special characters)
                    cursor.execute("SELECT id FROM City WHERE LOWER(city) = ?", (city_name,))
                    city = cursor.fetchone()

                    if city:
                        city_id = city[0]
                        print(f"Inserting into CityNews: city_id={city_id}, news_id={news_id}")
                        # Insert into CityNews table
                        cursor.execute("INSERT INTO CityNews (city_id, news_id) VALUES (?, ?)", (city_id, news_id))
                    else:
                        print(f"City {city_name} not found in the database.")
            else:
                print(f"No cities identified for news id {news_id}")

        except openai.error.OpenAIError as e:
            print(f"Error processing news id {news_id}: {str(e)}")
            continue
        except Exception as e:
            print(f"Unexpected error processing news id {news_id}: {str(e)}")
            continue

    # Commit the changes to the database
    try:
        conn.commit()
        print(f"Commit successful for the first {limit} news articles.")
    except Exception as e:
        print(f"Error committing to the database: {str(e)}")
    
    conn.close()
    print(f"Classification and assignment of the first {limit} news articles completed.")

# Execute the pipeline with limit set to 5
classify_and_assign_news(limit=5)
