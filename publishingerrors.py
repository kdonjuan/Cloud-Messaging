from google.cloud import pubsub_v1

PROJECT_ID = "your-gcp-project-id"
TOPIC_ID = "my-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

try:
    test_message = "Test message for debugging"
    future = publisher.publish(topic_path, test_message.encode("utf-8"))
    message_id = future.result()  # This will raise an error if publishing fails
    print(f"Message published successfully! ID: {message_id}")
except Exception as e:
    print(f"Error publishing message: {e}")
