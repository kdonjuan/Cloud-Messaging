import pytest
import logging
import time
from google.cloud import pubsub_v1

# ---------- CONFIG ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PROJECT_ID = "marine-actor-450915-b0"
SUBSCRIPTION_ID = "message-subscription"
TOPIC_ID = "message-topic"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

# ---------- FIXTURE ----------
@pytest.fixture
def publish_test_message():
    """
    Publishes a test message to the topic before the test runs.
    Returns the message string.
    """
    test_message = "Test message for PUBSUB_TC_002"
    future = publisher.publish(topic_path, test_message.encode("utf-8"))
    message_id = future.result()

    logging.info(f"Published test message: '{test_message}' (ID: {message_id})")

    # Wait a moment for message to propagate
    time.sleep(3)
    return test_message

# ---------- TEST ----------
def test_subscriber_retrieves_message(publish_test_message):
    """
    Test that the subscriber can retrieve the published message.
    """

    logging.info("Pulling messages from the subscription...")

    response = subscriber.pull(
        subscription=subscription_path,
        max_messages=1,
        timeout=10  # optional
    )

    assert len(response.received_messages) > 0, "❌ No messages retrieved from Pub/Sub"

    received_message = response.received_messages[0]
    message_data = received_message.message.data.decode("utf-8")

    logging.info(f"✅ Retrieved message: '{message_data}'")

    # Verify message content matches what was published
    assert message_data == publish_test_message, f"❌ Expected: '{publish_test_message}', Got: '{message_data}'"

    # Acknowledge the message so it's not redelivered
    ack_id = received_message.ack_id
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[ack_id])

    logging.info("✅ Message acknowledged successfully.")
