import yfinance as yf
import csv
from google.cloud import datastore, storage
from datetime import datetime

tsla = yf.Ticker("TSLA")
# historical_data = tsla.history(start='2023-01-01', end='2023-06-16')
historical_data = tsla.history(period='1day')

csv_file_name = 'tesla_stock.csv'

# Append data to the existing CSV file
with open(csv_file_name, 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    if csv_file.tell() == 0:  # Check if the file is empty
        writer.writerow(["Date", "Price", "Volume"])

    for index, row in historical_data.iterrows():
        date = index
        price = row['Close']
        volume = row['Volume']

        writer.writerow([date, price, volume])

storage_client = storage.Client()
bucket_name = 'sentiment-files'
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(csv_file_name)
blob.upload_from_filename(csv_file_name)

script_file_name = 'creation&upload.py'
blob = bucket.blob(script_file_name)
blob.upload_from_filename(script_file_name)

client = datastore.Client()
kind = 'tesla-data'

for index, row in historical_data.iterrows():
    date = index
    price = row['Close']
    volume = row['Volume']

    entity = datastore.Entity(client.key(kind))
    entity.update({
        "date": date,
        "price": price,
        "volume": volume
    })
    client.put(entity)

print("Data uploaded to Google Cloud Datastore and files uploaded to Google Cloud Storage.")