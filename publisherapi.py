import os
from flask import Flask, request, jsonify, render_template
from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
from db_config import get_db_connection
from config import PROJECT_ID, TOPIC_ID, GOOGLE_APPLICATION_CREDENTIALS
 
# Set up Flask app
app = Flask(__name__)
 
# Load service account credentials
credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
 
# Initialize the Pub/Sub publisher
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
 
# HTML form route (if using templates)
@app.route("/", methods=["GET"])
def home():
    return render_template("publisher.html")
 
# ✅ Fixed /publish route that accepts full message JSON
@app.route("/publish", methods=["POST"])
def publish_message():
    try:
        message = request.get_json()  # Expecting full JSON, not wrapped
        if not message:
            return jsonify({"error": "Missing JSON data"}), 400
 
        print("🔁 Received message to publish:", message)  # For debugging/logging
 
        # Convert the full message to JSON bytes and publish
        message_data = json.dumps(message).encode("utf-8")
        future = publisher.publish(topic_path, message_data)
        message_id = future.result()
 
        return jsonify({"message": "Message published successfully", "message_id": message_id}), 200
 
    except Exception as e:
        print("❌ Error publishing message:", e)
        return jsonify({"error": str(e)}), 500
 
# /messages route to retrieve from DB for Consumer UI
@app.route("/messages", methods=["GET"])
def get_messages():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
 
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
 
        return jsonify(messages), 200
    except Exception as e:
        print("❌ Error retrieving messages:", e)
        return jsonify({"error": str(e)}), 500
 
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)