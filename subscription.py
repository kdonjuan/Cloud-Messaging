# subscription.py

from google.cloud import pubsub_v1
import json
import logging
from db_config import get_db_connection
from config import PROJECT_ID, SUBSCRIPTION_ID

# Set up logging
logging.basicConfig(
    filename='subscriber.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Connect to Cloud SQL
conn = get_db_connection()
cursor = conn.cursor()

def is_duplicate(message_id):
    cursor.execute("SELECT COUNT(*) FROM messages WHERE message_id = %s", (message_id,))
    return cursor.fetchone()[0] > 0

def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        message_id = data.get("TransactionNumber")
        content = json.dumps(data)
        status = data.get("Status", "UNKNOWN")
        timestamp = data.get("TransactionDateTime", None)

        if not message_id:
            logging.warning("Message skipped due to missing TransactionNumber")
            message.ack()
            return

        if not is_duplicate(message_id):
            cursor.execute(
                "INSERT INTO messages (message_id, item_id, location, quantity, status, transaction_datetime, content, is_duplicate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    message_id,
                    data.get("ItemId"),
                    data.get("Location"),
                    data.get("Quantity"),
                    status,
                    timestamp,
                    content,
                    False
                )
            )
            conn.commit()
            logging.info(f"Message stored: {message_id}")
        else:
            logging.info(f"Duplicate message skipped: {message_id}")

        message.ack()

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        message.ack()

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
subscriber.subscribe(subscription_path, callback=callback)

logging.info("Subscriber is listening for messages.")
while True:
    pass
