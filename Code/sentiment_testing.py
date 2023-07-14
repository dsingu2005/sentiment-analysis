import pandas as pd
from google.cloud import language_v1

# Step 2: Install the required libraries
# Make sure you have the `google-cloud-language` library installed. You can install it by running the following command:
# pip install google-cloud-language

# Step 3: Import the necessary modules
import pandas as pd
from google.cloud import language_v1

# Step 4: Load the CSV file
df = pd.read_csv('news_articles.csv')

# Step 5: Initialize the Natural Language client
client = language_v1.LanguageServiceClient()

# Step 6: Perform sentiment analysis
df['Sentiment'] = ""

for index, row in df.iterrows():
    # Combine the title and body for sentiment analysis
    text = row["Article's"]
    
    # Perform sentiment analysis
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    df.at[index, 'Sentiment'] = response.document_sentiment.score

# Step 7: Save the results
df.to_csv('news_articles_with_sentiment.csv', index=False)
