import pytest
import logging
from google.cloud import pubsub_v1
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Google Cloud Pub/Sub setup
PROJECT_ID = "your-gcp-project-id"
TOPIC_ID = "my-topic"
SUBSCRIPTION_ID = "my-subscription"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


@pytest.fixture
def publish_test_message():
    """Publish a test message to the topic before the test runs"""
    test_message = "Test message for PUBSUB_TC_002"
    future = publisher.publish(topic_path, test_message.encode("utf-8"))
    message_id = future.result()
    logging.info(f"Published test message: {test_message} (ID: {message_id})")
    time.sleep(2)  # Give some time for message propagation
    return test_message


def test_subscriber_retrieves_message(publish_test_message):
    """Test that the subscriber can retrieve the published message"""
    response = subscriber.pull(subscription=subscription_path, max_messages=1)

    # Verify that at least one message is retrieved
    assert len(response.received_messages) > 0, "No messages retrieved from Pub/Sub"

    received_message = response.received_messages[0]
    message_data = received_message.message.data.decode("utf-8")

    # Log message
    logging.info(f"Retrieved message: {message_data}")

    # Verify that the received message matches the expected message
    assert message_data == publish_test_message, "Retrieved message does not match expected content"

    # Acknowledge the message
    ack_id = received_message.ack_id
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[ack_id])
    logging.info("Message acknowledged successfully")
