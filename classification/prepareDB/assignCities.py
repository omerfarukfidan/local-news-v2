import pyodbc
from app.database import get_db_connection

def assign_news_to_cities():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Select all news articles that are classified as local
    cursor.execute("SELECT id, content FROM News WHERE is_local = 1")
    rows = cursor.fetchall()

    for row in rows:
        news_id, content = row

        # Here we use a simple matching to find relevant cities
        # You could enhance this part using NLP techniques
        cursor.execute("SELECT id, city FROM City")
        cities = cursor.fetchall()

        for city in cities:
            city_id, city_name = city
            if city_name.lower() in content.lower():
                # If the city name is in the article content, create a relation in CityNews
                cursor.execute("INSERT INTO CityNews (city_id, news_id) VALUES (?, ?)", city_id, news_id)

    conn.commit()
    conn.close()
    print("Cities assigned to news articles successfully.")

assign_news_to_cities()
