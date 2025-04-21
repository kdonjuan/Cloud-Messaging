import os
from flask import Flask, request, jsonify, render_template
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from config import PROJECT_ID, TOPIC_ID
from db_config import get_db_connection
 
# Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
 
# Initialize Flask
app = Flask(__name__, template_folder=TEMPLATE_DIR)
 
# Load credentials
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials = service_account.Credentials.from_service_account_file(credentials_path)
 
# Create Pub/Sub publisher
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
 
# Serve HTML page
@app.route("/", methods=["GET"])
def home():
    return render_template("publisher.html")
 
# Handle POST requests to publish messages
@app.route("/publish", methods=["POST"])
def publish_message():
    try:
        data = request.get_json()
        message = data.get("message")
 
        if not message:
            return jsonify({"error": "Message is required"}), 400
 
        future = publisher.publish(topic_path, message.encode("utf-8"))
        message_id = future.result()
 
        return jsonify({"message": "Message published successfully", "message_id": message_id})
 
    except Exception as e:
        print("🔥 Error in /publish:", e)
        return jsonify({"error": str(e)}), 500
 
# ✅ Handle GET requests to retrieve messages
@app.route("/messages", methods=["GET"])
def get_messages():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()  # ✅ FIXED: removed dictionary=True
 
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
        print("🔥 Error in /messages:", e)
        return jsonify({"error": str(e)}), 500
 
# Run server
if __name__ == "__main__":
    app.run(debug=True, port=5001)