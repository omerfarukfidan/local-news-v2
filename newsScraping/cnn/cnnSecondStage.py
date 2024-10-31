import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the CSV file containing the links
links_df = pd.read_csv('cnn_article_links.csv')

# List to hold the news data
news_data = []

# Iterate over each link
for index, row in links_df.iterrows():
    url = row['url']
    
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Set the response encoding to utf-8
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title_tag = soup.find('h1', {'data-editable': 'headlineText'})
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Extract the content (paragraphs)
        paragraphs = soup.find_all('p', class_='paragraph')
        content = ' '.join([para.get_text(strip=True) for para in paragraphs])

        # Append the extracted data
        news_data.append({'title': title, 'content': content, 'url': url})
    else:
        print(f"Failed to retrieve article: {url}, status code: {response.status_code}")

# Create a DataFrame from the news data
news_df = pd.DataFrame(news_data)

# Save the news data to a new CSV file
news_df.to_csv('cnn_news_articles_extracted.csv', index=False)

print("Article titles and content have been extracted and saved to cnn_news_articles_extracted.csv")
