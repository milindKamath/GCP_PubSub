import base64
from google.cloud import storage

def getMessage(event, context):
     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     bucket_name = "exchange_info_bucket"
     fileName = "info.txt"
     client = storage.Client()

     bucket = client.bucket(bucket_name)
     bucket.storage_class = "COLDLINE"

     try:
          allBuckets = client.list_buckets()
          if bucket_name not in allBuckets:
               new_bucket = client.create_bucket(bucket, location="us")
     except:
          pass

     pubsub_message = base64.b64decode(event['data']).decode('utf-8')

     bucket = client.get_bucket(bucket_name)

     blob = bucket.blob(fileName)

     blob.upload_from_string(pubsub_message)

     print(pubsub_message)