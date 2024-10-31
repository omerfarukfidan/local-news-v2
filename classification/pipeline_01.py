import openai
import os
import sys
from dotenv import load_dotenv

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

# Function to classify news as local or global and determine relevant locations
def classify_and_assign_news():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Select all unclassified news articles
    cursor.execute("SELECT id, title, content FROM News")
    news_articles = cursor.fetchall()

    for article in news_articles:
        news_id, title, content = article

        # Prepare input for GPT-4o-mini
        prompt = f"Classify the following news article as 'local' or 'global' and specify the city or cities it is related to, if applicable.\nTitle: {title}\nContent: {content}\n"

        # Request classification from GPT-4o-mini
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that classifies news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )

            # Extract response
            output = response.choices[0].message['content'].strip().split('\n')
            classification = output[0].strip().lower()  # Expected to be either 'local' or 'global'

            if classification == 'local':
                # Extract city names from the output
                city_names = output[1:]  # Assuming subsequent lines contain city names

                for city_name in city_names:
                    city_name = city_name.strip()
                    if not city_name:
                        continue

                    # Fetch the city ID from the City table
                    cursor.execute("SELECT id FROM City WHERE city = ?", city_name)
                    city = cursor.fetchone()

                    if city:
                        city_id = city[0]
                        # Insert into CityNews table
                        cursor.execute("INSERT INTO CityNews (city_id, news_id) VALUES (?, ?)", city_id, news_id)
        except Exception as e:
            print(f"Error processing news id {news_id}: {str(e)}")
            continue

    # Commit the changes to the database
    conn.commit()
    conn.close()
    print("Classification and assignment of news articles completed.")

# Execute the pipeline
classify_and_assign_news()
