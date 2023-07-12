from google.cloud import storage

def delete_file(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
    print(f"File '{file_name}' deleted successfully from bucket '{bucket_name}'.")

bucket_name = 'sentiment-files'
file_name = 'tesla_stock.csv'
delete_file(bucket_name, file_name)
