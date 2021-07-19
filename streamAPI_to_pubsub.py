import requests
import json
from google.cloud import pubsub_v1
from google.oauth2 import service_account


class Stream_to_PUBSUB():

    def __init__(self):
        self.project_id = "peak-emblem-319723"
        self.topicName = "Currency_Exchange_Info"
        self.publisher = None
        self.topicName_created = None
        self.dataJson = ""
        self.credentials = service_account.Credentials.from_service_account_file("key/peak-emblem-319723-0d90f9eb6ad4.json")
        self.data = ""
        self.subscriptionName = "CurrencyInfo"

    def getRequest(self):
        try:
            response = requests.get("https://v6.exchangerate-api.com/v6/6aefed591b8b9cd998f940ae/latest/USD")
            if response.status_code == 200:
                self.data = response.text
                self.dataJson = json.loads(self.data)
        except:
            print("Invalid url/apikey")

    def create_pub_sub_topic(self):
        try:
            self.publisher = pubsub_v1.PublisherClient(credentials=self.credentials)
            self.topicName_created = 'projects/{project_id}/topics/{topic}'.format(
                project_id=self.project_id,
                topic=self.topicName,
            )

            self.publisher.create_topic(name=self.topicName_created)
        except:
            pass

    def callback(self, message):
        print("Message recevied from the topic", message.data)
        message.ack()

    def publish_to_topic(self):
        future = self.publisher.publish(self.topicName_created, str.encode(self.data), dataFormat="json")
        future.result()

    def create_subscriber(self):
        try:
            self.subscriptionName = 'projects/{project_id}/subscriptions/{sub}'.format(
                project_id=self.project_id,
                sub=self.subscriptionName,
            )

            with pubsub_v1.SubscriberClient(credentials=self.credentials) as subscriber:
                try:
                    subscriber.create_subscription(
                        name=self.subscriptionName, topic=self.topicName_created)
                except:
                    future = subscriber.subscribe(self.subscriptionName, self.callback)
                    future.result(timeout=2)
        except:
            pass


def startStreaming():
    sbs = Stream_to_PUBSUB()
    sbs.create_pub_sub_topic()
    sbs.create_subscriber()
    sbs.getRequest()
    sbs.publish_to_topic()


if __name__ == '__main__':
    startStreaming()