from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from flask_cors import CORS
from datetime import datetime
import uuid
import json
import os

from db_config import get_db_connection  # ✅ required to connect to Cloud SQL

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Replace with your GCP project and topic
PROJECT_ID = "marine-actor-450915-b0"
TOPIC_ID = "message-topic"

# Optional: set path to your service account credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service-account.json"

try:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
except Exception as e:
    print("Error initializing publisher:", e)
    topic_path = None

# ✅ Publish a message to Google Pub/Sub
@app.route('/publish', methods=['POST'])
def publish_message():
    if topic_path is None:
        return jsonify({"status": "Server misconfigured: topic not found"}), 500

    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'status': 'Message is empty'}), 400

        # Structure the message
        message_data = {
            "TransactionNumber": str(uuid.uuid4()),
            "ItemId": "ITEM-" + str(uuid.uuid4())[:8],
            "Location": "Warehouse A",
            "Quantity": 10,
            "Status": "SUCCESS",
            "TransactionDateTime": datetime.utcnow().isoformat(),
            "Note": user_message
        }

        future = publisher.publish(topic_path, json.dumps(message_data).encode("utf-8"))
        future.result()

        return jsonify({
            "status": "Message published successfully!",
            "message": message_data
        })

    except Exception as e:
        print("Publish error:", e)
        return jsonify({
            "status": "Error publishing message",
            "error": str(e)
        }), 500

# ✅ Retrieve messages from the database for Consumer UI
@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_id, location, quantity, transaction_datetime, message_id
            FROM messages
            ORDER BY transaction_datetime DESC
            LIMIT 100
        """)
        rows = cursor.fetchall()

        messages = []
        for row in rows:
            messages.append({
                "item_id": row[0],
                "location": row[1],
                "quantity": row[2],
                "transaction_time": row[3].strftime("%Y-%m-%d %H:%M:%S") if row[3] else "",
                "transaction_number": row[4]
            })

        return jsonify(messages)

    except Exception as e:
        print("Fetch error:", e)
        return jsonify({
            "status": "Error fetching messages",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server running on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
