from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
import logging
from db_config import get_db_connection
from config import PROJECT_ID, TOPIC_ID, GOOGLE_APPLICATION_CREDENTIALS

# Set up logging
logging.basicConfig(
    filename='api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route('/publish', methods=['POST'])
def publish_message():
    try:
        data = request.json
        if not data:
            logging.warning("Missing JSON in /publish request.")
            return jsonify({"error": "Request must contain JSON data"}), 400

        message_data = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, message_data)
        message_id = future.result()

        logging.info(f"Published message with ID: {message_id}")
        return jsonify({"message": "Message published successfully", "message_id": message_id}), 200

    except Exception as e:
        logging.error(f"Error publishing message: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT message_id, item_id, location, quantity, status, transaction_datetime, is_duplicate, created_at
            FROM messages
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()

        messages = []
        for row in rows:
            messages.append({
                "TransactionNumber": row["message_id"],
                "ItemID": row["item_id"],
                "Location": row["location"],
                "Quantity": row["quantity"],
                "Status": row["status"],
                "TransactionDateTime": row["transaction_datetime"].isoformat() if row["transaction_datetime"] else None,
                "isDuplicate": row["is_duplicate"],
                "ReceivedAt": row["created_at"].isoformat()
            })

        logging.info("Retrieved messages from database.")
        return jsonify(messages), 200

    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
