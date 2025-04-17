from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from flask_cors import CORS
from datetime import datetime
import uuid
import json
import os

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

@app.route('/publish', methods=['POST'])
def publish_message():
    if topic_path is None:
        return jsonify({"status": "Server misconfigured: topic not found"}), 500

    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'status': 'Message is empty'}), 400

        # Structure the message to match what subscription.py expects
        message_data = {
            "TransactionNumber": str(uuid.uuid4()),
            "ItemId": "ITEM-" + str(uuid.uuid4())[:8],
            "Location": "Warehouse A",
            "Quantity": 10,
            "Status": "SUCCESS",
            "TransactionDateTime": datetime.utcnow().isoformat(),
            "Note": user_message
        }

        # Publish the message
        future = publisher.publish(topic_path, json.dumps(message_data).encode("utf-8"))
        future.result()  # Block until it's published

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server running on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)

