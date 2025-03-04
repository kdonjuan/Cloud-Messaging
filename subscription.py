from google.cloud import pubsub_v1
import json
import mysql.connector  # MySQL Connector
from config import PROJECT_ID, SUBSCRIPTION_ID, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Connect to MySQL database
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

# Function to check for duplicates
def is_duplicate(message_id):
    cursor.execute("SELECT COUNT(*) FROM messages WHERE message_id = %s", (message_id,))
    return cursor.fetchone()[0] > 0

# Function to process messages
def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    message_id = data.get("TransactionNumber")

    if not is_duplicate(message_id):
        cursor.execute(
            "INSERT INTO messages (message_id, content) VALUES (%s, %s)",
            (message_id, json.dumps(data))
        )
        conn.commit()
        message.ack()  # Acknowledge message so it's removed from queue
        print(f"Processed message: {message_id}")
    else:
        print(f"Duplicate message detected: {message_id}")
        message.ack()  # Acknowledge but don’t store duplicate

# Start subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
subscriber.subscribe(subscription_path, callback=callback)

print("Listening for messages...")
while True:
    pass  # Keeps the script running
