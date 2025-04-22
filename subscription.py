from google.cloud import pubsub_v1
import json
import logging
import time
from db_config import get_db_connection
from config import PROJECT_ID, SUBSCRIPTION_ID
 
logging.basicConfig(filename='subscriber.log', level=logging.INFO)
 
conn = get_db_connection()
cursor = conn.cursor()
 
def is_duplicate(message_id):
    cursor.execute("SELECT COUNT(*) FROM messages WHERE message_id = %s", (message_id,))
    return cursor.fetchone()[0] > 0
 
def callback(message):
    print("📥 Received a message!")
    try:
        data = json.loads(message.data.decode("utf-8"))
        message_id = data.get("TransactionNumber")
        status = data.get("Status", "UNKNOWN")
        timestamp = data.get("TransactionDateTime")
 
        if not message_id:
            print("⚠️ Skipped: Missing TransactionNumber")
            message.ack()
            return
 
        if not is_duplicate(message_id):
            cursor.execute("""
                INSERT INTO messages (message_id, item_id, location, quantity, status, transaction_datetime, content, is_duplicate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                message_id,
                data.get("ItemId"),
                data.get("Location"),
                data.get("Quantity"),
                status,
                timestamp,
                json.dumps(data),
                False
            ))
            conn.commit()
            print(f"✅ Message stored: {message_id}")
        else:
            print(f"⚠️ Duplicate message skipped: {message_id}")
 
        message.ack()
    except Exception as e:
        logging.exception("❌ Error processing message")
        message.ack()
 
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
 
print("🔊 Subscriber is running and waiting for messages...")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    subscriber.close()