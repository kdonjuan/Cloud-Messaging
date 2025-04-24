from google.cloud import pubsub_v1
import logging

project_id = "your-project-id"
topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

message_data = "Test Message"
message_id = "12345"  # Unique ID for deduplication

try:
    future = publisher.publish(topic_path, message_data.encode("utf-8"), message_id=message_id)
    print(f"Published message ID: {future.result()}")
except Exception as e:
    logging.error(f"Error publishing message: {e}")


