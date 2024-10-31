from flask import Blueprint, jsonify, request
from flask_cors import CORS
from app.database import get_db_connection

main_routes = Blueprint('main_routes', __name__)
CORS(main_routes)  # Enable CORS specifically for this blueprint

# Route to fetch news by city name
@main_routes.route('/news/<city_name>', methods=['GET'])
def get_news_by_city(city_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT * 
    FROM news_by_city_view
    WHERE city = %s
    '''

    cursor.execute(query, (city_name,))
    rows = cursor.fetchall()

    news_list = []
    for row in rows:
        news_item = {
            'NewsID': row[0],
            'city': row[1],
            'title': row[2],
            'content': row[3]
        }
        news_list.append(news_item)

    conn.close()
    return jsonify(news_list)

# Route to fetch distinct cities for dropdown
@main_routes.route('/distinct-cities', methods=['GET'])
def get_distinct_cities():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM distinct_cities_view")
    rows = cursor.fetchall()

    distinct_cities = [row[0] for row in rows]

    conn.close()
    return jsonify(distinct_cities)

# Route to fetch news URL by news ID
@main_routes.route('/news-url/<int:news_id>', methods=['GET'])
def get_news_url(news_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT url 
    FROM news_url_by_id_view
    WHERE id = %s
    '''

    cursor.execute(query, (news_id,))
    row = cursor.fetchone()

    if row:
        news_url = {'url': row[0]}
    else:
        news_url = {'error': 'News not found'}

    conn.close()
    return jsonify(news_url)
