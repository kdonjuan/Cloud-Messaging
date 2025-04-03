from google.cloud import pubsub_v1
import logging
import os
import uuid

# Set up logging
logging.basicConfig(filename='publisher_test.log', level=logging.INFO)

# Set up Google Cloud credentials (if not set globally)
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-key.json'

# Define project ID and topic name
project_id = "your-gcp-project-id"
topic_id = "message-topic"

# Construct message data
message_data = {
    "transaction_number": str(uuid.uuid4()),
    "content": "Test message from automated script"
}

# Publish message
def publish_message():
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)

        # Publish the message
        future = publisher.publish(
            topic_path,
            str(message_data).encode("utf-8"),
            origin="automated-test",
            username="test-script"
        )
        message_id = future.result()
        logging.info(f"Message published successfully. Message ID: {message_id}")
        print("✅ Test Passed: Message published.")
    except Exception as e:
        logging.error(f"Test Failed: Could not publish message. Error: {e}")
        print("❌ Test Failed: See log for details.")

publish_message()
