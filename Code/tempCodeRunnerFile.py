import requests
import yfinance as yf
import csv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')

tick = yf.Ticker("TSLA")
news = tick.news
news_array = []

for article in news:
    link = article["link"]
    try:
        article_response = requests.get(link)
        soup = BeautifulSoup(article_response.text, "html.parser")
        news_body = soup.find("div", attrs={'class': 'caas-body'})
        if news_body:
            news_text = news_body.get_text(separator='\n\n')
        else:
            news_text = "No article found"

        pub_date_match = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", link)
        if pub_date_match:
            pub_date_str = f"{pub_date_match.group(1)}-{pub_date_match.group(2)}-{pub_date_match.group(3)}"
            if pub_date_str == yesterday_str:
                news_array.append(news_text)
        else:
            news_array.append(news_text)

    except:
        continue

csv_file = "news_articles.csv"
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["News Body"])
    for news_text in news_array:
        writer.writerow([news_text])

print(f"News articles from {yesterday_str} have been saved to '{csv_file}'.")
