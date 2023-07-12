from google.cloud import datastore

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

def main():
    news_csv_path = 'news_articles.csv'
    news_kind = 'tesla-data'
    upload_csv_to_datastore(news_csv_path, news_kind)

    stock_csv_path = 'tesla_stock.csv'
    stock_kind = 'tesla-data'
    upload_csv_to_datastore(stock_csv_path, stock_kind)

if __name__ == '__main__':
    main()
