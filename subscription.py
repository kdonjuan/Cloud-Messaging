from google.cloud import pubsub_v1
import json
import logging
import time
import traceback
from db_config import get_db_connection
from config import PROJECT_ID, SUBSCRIPTION_ID
 
# Optional log file
logging.basicConfig(filename='subscriber.log', level=logging.INFO)
 
conn = get_db_connection()
cursor = conn.cursor()
 
def is_duplicate(message_id):
    cursor.execute("SELECT COUNT(*) AS count FROM messages WHERE message_id = %s", (message_id,))
    result = cursor.fetchone()
    return result["count"] if result else 0
 
def callback(message):
    print("📥 Received a message!")
    try:
        data = json.loads(message.data.decode("utf-8"))
        message_id = data.get("TransactionNumber")
 
        if not message_id:
            print("⚠️ Skipped: Missing TransactionNumber")
            message.ack()
            return
 
        if is_duplicate(message_id):
            print(f"⚠️ Duplicate message skipped: {message_id}")
            message.ack()
            return
 
        cursor.execute("""
            INSERT INTO messages (
                message_id, item_id, location, quantity, status,
                transaction_datetime, content, is_duplicate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            message_id,
            data.get("ItemId"),
            data.get("Location"),
            data.get("Quantity"),
            data.get("Status"),
            data.get("TransactionDateTime"),  # Direct from input
            json.dumps(data),
            False
        ))
 
        conn.commit()
        print(f"✅ Message stored: {message_id}")
 
    except Exception as e:
        print("❌ Error while storing message:")
        traceback.print_exc()
    finally:
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