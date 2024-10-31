import pandas as pd

# Define the file paths
cnn_csv_path = r"C:\Users\omerf\Documents\LocalNews\LocalNews\newsDataset\cnn\cnn_news_articles_extracted.csv"
usa_today_csv_path = r"C:\Users\omerf\Documents\LocalNews\LocalNews\newsDataset\usaToday\news_articles_content.csv"

# Read the CSV files
cnn_df = pd.read_csv(cnn_csv_path)
usa_today_df = pd.read_csv(usa_today_csv_path)

# Combine the data
combined_df = pd.concat([cnn_df, usa_today_df], ignore_index=True)

# Save the combined data to a new CSV file
combined_csv_path = r"C:\Users\omerf\Documents\LocalNews\LocalNews\newsDataset\combined_news_articles.csv"
combined_df.to_csv(combined_csv_path, index=False)

print(f"CSV files have been successfully combined and saved to {combined_csv_path}.")
