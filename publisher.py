from google.cloud import pubsub_v1
import json

# Set project and topic name
project_id = "marine-actor-450915-b0"  # Your actual project ID
topic_id = "message-topic"

# Initialize publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Create a sample message
message_data = {
    "message_id": "123456",
    "content": "Hello, this is a test message!",
    "timestamp": "2025-02-20T12:00:00Z"
}

# Convert message to JSON and publish
future = publisher.publish(topic_path, json.dumps(message_data).encode("utf-8"))
print(f"Message published: {future.result()}")
