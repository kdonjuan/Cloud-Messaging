from google.cloud import pubsub_v1
import json
import logging
import time
import traceback
from db_config import get_db_connection
from config import PROJECT_ID, SUBSCRIPTION_ID
 
# Set up logging (optional)
logging.basicConfig(filename='subscriber.log', level=logging.INFO)
 
# Database connection
conn = get_db_connection()
cursor = conn.cursor()
 
# ✅ Check for duplicate based on 4 fields (excluding TransactionNumber)
def is_duplicate(item_id, location, quantity, datetime_str):
    cursor.execute("""
        SELECT COUNT(*) AS count FROM messages
        WHERE item_id = %s AND location = %s AND quantity = %s AND transaction_datetime = %s
    """, (item_id, location, quantity, datetime_str))
    result = cursor.fetchone()
    return result["count"] > 0
 
# Handle messages from Pub/Sub
def callback(message):
    print("📥 Received a message!")
    try:
        data = json.loads(message.data.decode("utf-8"))
        message_id = data.get("TransactionNumber")
 
        if not message_id:
            print("⚠️ Skipped: Missing TransactionNumber")
            message.ack()
            return
 
        item_id = data.get("ItemId")
        location = data.get("Location")
        quantity = data.get("Quantity")
        transaction_datetime = data.get("TransactionDateTime")
 
        # ✅ Check for content-based duplicate
        duplicate = is_duplicate(item_id, location, quantity, transaction_datetime)
        if duplicate:
            print(f"⚠️ Duplicate content detected for ItemID {item_id} at {transaction_datetime}")
 
        # Store message
        cursor.execute("""
            INSERT INTO messages (
                message_id, item_id, location, quantity,
                transaction_datetime, content, is_duplicate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            message_id,
            item_id,
            location,
            quantity,
            transaction_datetime,
            json.dumps(data),
            duplicate
        ))
 
        conn.commit()
        print(f"✅ Message stored: {message_id}")
 
    except Exception as e:
        print("❌ Error while storing message:")
        traceback.print_exc()
    finally:
        message.ack()
 
# Start the subscriber
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