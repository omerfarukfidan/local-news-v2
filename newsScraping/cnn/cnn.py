import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the CNN homepage
url = 'https://edition.cnn.com/'
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to retrieve the CNN homepage: {response.status_code}")
else:
    # Step 2: Parse the homepage content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 3: Find all article links
    articles = soup.find_all('a', href=True)

    # List to hold article URLs
    article_links = []

    # Step 4: Filter and collect links
    for article in articles:
        link = article['href']
        # Check if the link points to a news article
        if link.startswith('/'):
            link = 'https://edition.cnn.com' + link  # Complete the URL
        if 'cnn.com' in link and link not in article_links:
            article_links.append(link)

    # Step 5: Save the links to a CSV file
    links_df = pd.DataFrame(article_links, columns=['url'])
    links_df.to_csv('cnn_article_links.csv', index=False)

    print("Article links scraping completed and saved to cnn_article_links.csv")
