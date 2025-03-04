from google.cloud import pubsub_v1
import json
from config import PROJECT_ID, TOPIC_ID  # Import project configuration

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

message = {
    "TransactionNumber": "12345",
    "content": "Test message"
}

publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
print("Message published.")
