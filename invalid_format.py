from google.cloud import pubsub_v1
import logging

project_id = "marine-actor-450915-b0"
topic_id = "message-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Send an invalid message (string instead of proper JSON or missing fields)
bad_message = "INVALID_MESSAGE_NO_JSON"

try:
    future = publisher.publish(topic_path, bad_message.encode("utf-8"))
    future.result()
    print("Message sent (intentionally invalid).")
except Exception as e:
    logging.error(f"Publishing failed: {e}")
