import pandas as pd
import yfinance as yf
import csv
import requests
from bs4 import BeautifulSoup
import os
import time
from google.cloud import datastore

def append_yesterdays_article(self) -> None:
        # gets yesterdays date 
        # and gets the article from that date
        tick = yf.Ticker(self.name)
        news = tick.news
        news_array = []
        date_array = []
        title_array = []
        num = 1
        #gets the date in the form of "Month Day, Year"
        yesterday = time.strftime("%B %d, %Y", time.localtime(time.time() - 86400))
        today = time.strftime("%B %d, %Y", time.localtime(time.time()))
        for i in news:
            link = i["link"]
            title = i["title"]
            article = requests.get(link)
            soup = BeautifulSoup(article.text,"html.parser")
            date = soup.find("div",attrs={'class': 'caas-attr-time-style'})
            news = soup.find("div",attrs={'class': 'caas-body'})

            if(news == None):
                news_array.append(["No Article"])
                date_array.append(["No Date"])
                title_array.append(["No Title"])
            else:
                if(yesterday in date.text or today in date.text):
                    news_text = news.get_text(separator='\n\n')
                    news_array.append([news_text])
                    date_array.append([date.text])
                    title_array.append([title])
                
        with open(self.file_name3,"a",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Article's"])
                    
            for article in news_array:
                
                if(article == ["No Article"]):
                    continue
                else:
                    writer.writerow([f"Article {num}'s - Body | date published: {date_array[num-1]}"])
                    writer.writerow([f"Title: {title_array[num-1]}"])
                    writer.writerow(article)     
                    num += 1
                          
        print("\nSuccess!\n")
        print(f"{self.file_name3} has been created\n")

