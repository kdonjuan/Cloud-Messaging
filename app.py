from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can connect

# Replace with your Google Cloud project ID and topic name
PROJECT_ID = "marine-actor-450915-b0"
SUBSCRIPTION_ID = "message-subscription"
TOPIC_ID = "message-topic"
# Optional: Set credentials manually
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account.json'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'status': 'Message is empty'}), 400

    future = publisher.publish(topic_path, message.encode('utf-8'))
    future.result()  # Wait for it to complete

    return jsonify({'status': 'Message published successfully!'})

if __name__ == '__main__':
    app.run(debug=True)

