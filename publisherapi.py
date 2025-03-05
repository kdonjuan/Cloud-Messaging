from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
from config import PROJECT_ID, TOPIC_ID, GOOGLE_APPLICATION_CREDENTIALS

app = Flask(__name__)

# Initialize the Pub/Sub publisher client
credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route('/publish', methods=['POST'])
def publish_message():
    try:
        # Get the message data from the request body
        data = request.json
        message = data.get("message")

        if not message:
            return jsonify({"error": "Message is required"}), 400

        # Convert the message to a byte string
        message_data = json.dumps({"message": message}).encode("utf-8")

        # Publish the message to the Pub/Sub topic
        future = publisher.publish(topic_path, message_data)

        # Wait for the message to be published and get the message ID
        message_id = future.result()

        return jsonify({"message": "Message published successfully", "message_id": message_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
