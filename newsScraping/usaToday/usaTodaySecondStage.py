import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the article links from the CSV file
articles_df = pd.read_csv('article_links.csv')

# List to hold article contents
article_contents = []

# Step 1: Iterate through each URL and fetch the content
for index, row in articles_df.iterrows():
    url = row['url']
    
    # Fetch the article page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve article at {url}: {response.status_code}")
        continue
    
    # Parse the content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 2: Extract the article title and content
    title = soup.find('h1', class_='display-2').text.strip() if soup.find('h1', class_='display-2') else 'No Title'
    
    # Extract all paragraphs
    paragraphs = soup.find_all('p')
    content = ' '.join([para.text.strip() for para in paragraphs if para.text.strip()])

    # Step 3: Append the title, content, and URL to the list
    article_contents.append({'title': title, 'content': content, 'url': url})

# Step 4: Create a DataFrame and save to CSV
contents_df = pd.DataFrame(article_contents)
contents_df.to_csv('news_articles_content.csv', index=False)

print("Article contents scraping completed and saved to news_articles_content.csv")
