import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the news site
base_url = "https://eu.usatoday.com/news/nation/"
# List to hold all the article titles and links
articles = []

# Step 1: Get the main page content
response = requests.get(base_url)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to retrieve the webpage: {response.status_code}")
else:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 2: Find all article links
    # Adjusting the selector to specifically target the correct elements
    for link in soup.find_all('a', href=True):
        # Check if the link is an article link
        if 'story' in link['href']:
            article_url = link['href']
            # Ensure the URL is complete
            if not article_url.startswith('http'):
                article_url = 'https://eu.usatoday.com' + article_url
            
            title = link.find('div', class_='p1-title-spacer').text.strip() if link.find('div', class_='p1-title-spacer') else 'No Title'
            
            # Append the article title and URL to the list
            articles.append({'title': title, 'url': article_url})

    # Step 3: Create a DataFrame and save to CSV
    df = pd.DataFrame(articles)
    df.to_csv('article_links.csv', index=False)

    print("Scraping completed and saved to article_links.csv")
