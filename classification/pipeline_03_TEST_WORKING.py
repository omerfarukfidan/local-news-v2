import os
import sys
import random

# Add the root directory to sys.path to make sure 'app' is found
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

try:
    from app.database import get_db_connection
except ModuleNotFoundError as e:
    print(f"Module import failed: {e}")
    sys.exit(1)

# Mock function for testing
def mock_classification(title, content):
    """ Mock function to simulate OpenAI classification. """
    classification = random.choice(["local", "global"])
    city_names = ["New York", "Los Angeles"] if classification == "local" else []
    return classification, city_names

# Function to classify news as local or global and determine relevant locations
def classify_and_assign_news():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Select all unclassified news articles
    cursor.execute("SELECT id, title, content FROM News")
    news_articles = cursor.fetchall()

    # Process only the first 10 records for testing
    for article in news_articles[:10]:
        news_id, title, content = article

        # Use mock classification function
        classification, city_names = mock_classification(title, content)

        if classification == 'local':
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

    # Commit the changes to the database
    conn.commit()
    conn.close()
    print("Classification and assignment of news articles completed for the first 10 records.")

# Execute the pipeline
classify_and_assign_news()
