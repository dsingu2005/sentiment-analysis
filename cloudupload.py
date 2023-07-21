import yfinance as yf
import csv
from google.cloud import datastore, storage
from datetime import datetime

def upload_csv_to_datastore(file_path, kind):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_data = file.read()

    # Create a Datastore client using the service account credentials
    client = datastore.Client.from_service_account_json('sentiment-analysis-379200-6be709076826.json')

    # Create an entity for each row in the CSV file
    rows = csv_data.split('\n')
    for row in rows:
        values = row.split(',')
        entity = datastore.Entity(client.key(kind))

        for i, value in enumerate(values):
            entity[str(i)] = value

        client.put(entity)

def delete_file(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
    print(f"File '{file_name}' deleted successfully from bucket '{bucket_name}'.")

def main():
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

    # Upload 'tesla_stock.csv' to Google Cloud Storage
    blob = bucket.blob(csv_file_name)
    blob.upload_from_filename(csv_file_name)

    # Upload 'news_articles.csv' to Google Cloud Storage
    news_csv_file = 'news_articles.csv'
    blob = bucket.blob(news_csv_file)
    blob.upload_from_filename(news_csv_file)

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

    news_csv_path = 'news_articles.csv'
    news_kind = 'tesla-data'
    upload_csv_to_datastore(news_csv_path, news_kind)

    stock_csv_path = 'tesla_stock.csv'
    stock_kind = 'tesla-data'
    upload_csv_to_datastore(stock_csv_path, stock_kind)

    # Uncomment these lines of code in order to delete the uploaded files
    # delete_file(bucket_name, csv_file_name)
    # delete_file(bucket_name, news_csv_file)

if __name__ == '__main__':
    main()
