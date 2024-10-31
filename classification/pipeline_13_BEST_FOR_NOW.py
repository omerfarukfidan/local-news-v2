import openai
import os
import sys
from dotenv import load_dotenv
import re
import csv

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

# Function to normalize city names for more flexible matching
def normalize_city_name(city_name):
    return re.sub(r'[^a-zA-Z\s]', '', city_name).strip().lower()

# Function to get the global city ID (which is set to 31121)
def get_global_city_id():
    return 31121

# Function to classify news by relevant American cities and write results to CSV
def classify_and_assign_news(csv_filename="news_classification.csv"):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the global city ID
    global_city_id = get_global_city_id()

    # Prepare CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['news_id', 'title', 'content', 'city']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Select all unclassified news articles
        query = "SELECT id, title, content FROM News"
        cursor.execute(query)
        news_articles = cursor.fetchall()

        for article in news_articles:
            news_id, title, content = article

            # Prepare input for GPT-4 or fallback to GPT-3.5-turbo
            prompt = f"Identify the relevant American city or cities for this news article. If no relevant American city is found, return 'Global'. Only list the city names or the word 'Global', and nothing else.\nTitle: {title}\nContent: {content}"

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

                # Extract response (cities or 'Global')
                output = response['choices'][0]['message']['content'].strip().split('\n')
                city_names = [normalize_city_name(city) for city in output if city.strip()]

                if city_names:
                    if "global" in city_names:  # If 'Global' is returned
                        print(f"News id {news_id} marked as global.")
                        # Check if the global entry already exists
                        cursor.execute("SELECT COUNT(*) FROM CityNews WHERE city_id = ? AND news_id = ?", (global_city_id, news_id))
                        if cursor.fetchone()[0] == 0:
                            # Insert global news with the global city_id into the database
                            cursor.execute("INSERT INTO CityNews (city_id, news_id) VALUES (?, ?)", (global_city_id, news_id))

                        # Write 'global' result to the CSV file
                        writer.writerow({
                            'news_id': news_id,
                            'title': title,
                            'content': content,
                            'city': 'Global'
                        })
                    else:
                        for city_name in city_names:
                            print(f"Processing city: {city_name}")

                            # Find an exact match for the city name
                            cursor.execute("SELECT id, city FROM City WHERE LOWER(city) = ?", (city_name,))
                            city = cursor.fetchone()

                            if city:
                                city_id, matched_city_name = city
                                print(f"Matched city: {matched_city_name}, Inserting into CityNews: city_id={city_id}, news_id={news_id}")
                                # Check if the entry already exists
                                cursor.execute("SELECT COUNT(*) FROM CityNews WHERE city_id = ? AND news_id = ?", (city_id, news_id))
                                if cursor.fetchone()[0] == 0:
                                    # Insert into CityNews table
                                    cursor.execute("INSERT INTO CityNews (city_id, news_id) VALUES (?, ?)", (city_id, news_id))

                                # Write the result to the CSV file
                                writer.writerow({
                                    'news_id': news_id,
                                    'title': title,
                                    'content': content,
                                    'city': matched_city_name
                                })
                            else:
                                print(f"City {city_name} not found in the database.")
                                # Write result to CSV even if no match in the database
                                writer.writerow({
                                    'news_id': news_id,
                                    'title': title,
                                    'content': content,
                                    'city': 'Not Found'
                                })
                else:
                    print(f"No cities identified for news id {news_id}")
                    writer.writerow({
                        'news_id': news_id,
                        'title': title,
                        'content': content,
                        'city': 'No City Identified'
                    })

            except openai.error.OpenAIError as e:
                print(f"Error processing news id {news_id}: {str(e)}")
                continue
            except Exception as e:
                print(f"Unexpected error processing news id {news_id}: {str(e)}")
                continue

    # Commit the changes to the database
    try:
        conn.commit()
        print(f"Commit successful for all news articles.")
    except Exception as e:
        print(f"Error committing to the database: {str(e)}")
    
    conn.close()
    print(f"Classification and assignment of all news articles completed.")

# Execute the pipeline for all records
classify_and_assign_news()
