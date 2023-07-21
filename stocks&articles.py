import pandas as pd
import yfinance as yf
import csv
import requests
from bs4 import BeautifulSoup
import os
import time
from google.cloud import datastore

# Replace '.json' with your Google Cloud credentials file path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sentiment-analysis-379200-6be709076826.json'
storage_client = datastore.Client()

# File names for CSV files to store data
STOCK_FILE = "stock.csv"
NEWS_HEADLINES_FILE = "news.csv"
ARTICLES_FILE = "news_articles.csv"

class StockInfo:
    def __init__(self, name, filename=STOCK_FILE, filename2=NEWS_HEADLINES_FILE, filename3=ARTICLES_FILE):
        # Constructor to initialize the StockInfo class object
        self.name = name
        self.file_name = filename
        self.file_name2 = filename2
        self.file_name3 = filename3

    def stock_to_csv(self, period="1d"):
        # Function to fetch stock data for a given period and save it to a CSV file
        try:
            tick = yf.Ticker(self.name)
            stock_data = tick.history(period=period)
            stock_data.drop(columns=["Dividends", "Stock Splits"], inplace=True)
            stock_data.to_csv(self.file_name, index=False)
            print("Success!")
            print(f"{self.file_name} has been created")
        except Exception as e:
            print(f"Error: {e}")

    def news_to_csv(self):
        # Function to fetch news headlines for a stock and save them to a CSV file
        try:
            tick = yf.Ticker(self.name)
            news = tick.news

            with open(self.file_name2, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Publisher", "Link"])
                for article in news:
                    title = article["title"]
                    publisher = article["publisher"]
                    link = article["link"]

                    writer.writerow([title, publisher, link])
            print("Success!")
            print(f"{self.file_name2} has been created")
        except Exception as e:
            print(f"Error: {e}")

    def article_to_csv(self):
        # Function to fetch full news articles for a stock and save them to a CSV file
        try:
            tick = yf.Ticker(self.name)
            news = tick.news
            news_array = []

            for article in news:
                link = article["link"]
                article_response = requests.get(link)
                soup = BeautifulSoup(article_response.text, "html.parser")
                news_body = soup.find("div", attrs={'class': 'caas-body'})

                if news_body is not None:
                    news_text = news_body.get_text(separator='\n\n')
                else:
                    news_text = "No article found"

                news_array.append([news_text])

            with open(self.file_name3, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Article's"])
                num = 1
                for article in news_array:
                    writer.writerow([f"Article {num}'s - Body"])
                    writer.writerow(article)
                    num += 1

            print("Success!")
            print(f"{self.file_name3} has been created")
        except Exception as e:
            print(f"Error: {e}")

    def get_yesterdays_article(self):
        # Function to fetch yesterday's news articles for a stock and save them to a CSV file
        try:
            yesterday = time.strftime("%B %d, %Y", time.localtime(time.time() - 86400))
            today = time.strftime("%B %d, %Y", time.localtime(time.time()))
            news_array = []
            title_array = []
            num = 1

            tick = yf.Ticker(self.name)
            news = tick.news

            for article in news:
                title = article["title"]
                link = article["link"]
                article_response = requests.get(link)
                soup = BeautifulSoup(article_response.text, "html.parser")
                date = soup.find("div", attrs={'class': 'caas-attr-time-style'})
                news_body = soup.find("div", attrs={'class': 'caas-body'})

                if date and (yesterday in date.text or today in date.text):
                    if news_body is not None:
                        news_text = news_body.get_text(separator='\n\n')
                    else:
                        news_text = "No article found"

                    news_array.append(news_text)
                    title_array.append(title)

            with open(self.file_name3, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Article's"])

                for num, article_text in enumerate(news_array, 1):
                    writer.writerow([f"Article {num}'s - Body"])
                    writer.writerow([f"Title: {title_array[num - 1]}"])
                    writer.writerow([article_text])

            print("\nSuccess!\n")
            print(f"{self.file_name3} has been created\n")
        except Exception as e:
            print(f"Error: {e}")

    def append_yesterdays_article(self):
        # Function to append yesterday's news articles to the existing "news_articles.csv" file
        try:
            yesterday = time.strftime("%B %#d, %Y", time.localtime(time.time() - 86400))
            today = time.strftime("%B %#d, %Y", time.localtime(time.time()))
            news_array = []
            date_array = []
            title_array =  []

            tick = yf.Ticker(self.name)
            news = tick.news

            for article in news:
                link = article["link"]
                title = article["title"]
                article_response = requests.get(link)

                soup = BeautifulSoup(article_response.text, "html.parser")
                date = soup.find("div", attrs={'class': 'caas-attr-time-style'})
                news_body = soup.find("div", attrs={'class': 'caas-body'})

                if date and (yesterday in date.text or today in date.text):
                    if news_body is not None:
                        news_text = news_body.get_text(separator='\n\n')
                    else:
                        news_text = "No article found"

                    news_array.append(news_text)
                    date_array.append(date.text)
                    title_array.append(title)

            with open(self.file_name3, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Article's"])

                for i in range(len(news_array)):
                    writer.writerow([f"Article {i + 1}'s - Body | date published: {date_array[i]}, title: {title_array[i]}"])
                    writer.writerow([news_array[i]])

            print("\nSuccess!\n")
            print(f"{self.file_name3} has been created\n")
        except Exception as e:
            print(f"Error: {e}")

    def clear_csv(self, filename):
        # Function to clear a CSV file
        try:
            os.remove(filename)
            print("Success!")
            print(f"{filename} has been deleted")
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Example usage of StockInfo class to fetch stock data and news articles for a specific ticker
    stock = StockInfo("UPDATE TICKER HERE")

    # Clear CSV files before creating/updating them
    stock.clear_csv(STOCK_FILE)
    stock.clear_csv(ARTICLES_FILE)

    # Fetch and save stock information to CSV
    stock.stock_to_csv()

    # Fetch and save news headlines to CSV
    stock.news_to_csv()

    # Fetch and save full news articles to CSV
    stock.article_to_csv()

    # Append yesterday's news articles to the existing "news_articles.csv" file
    stock.append_yesterdays_article()
