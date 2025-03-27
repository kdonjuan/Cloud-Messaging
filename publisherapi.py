from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
import mysql.connector
from config import PROJECT_ID, TOPIC_ID, GOOGLE_APPLICATION_CREDENTIALS, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

# Initialize the Pub/Sub publisher client
credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route('/publish', methods=['POST'])
def publish_message():
    try:
        data = request.json
        message = data.get("message")

        if not message:
            return jsonify({"error": "Message is required"}), 400

        message_data = json.dumps({"message": message}).encode("utf-8")
        future = publisher.publish(topic_path, message_data)
        message_id = future.result()

        return jsonify({"message": "Message published successfully", "message_id": message_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT message_id, content, created_at FROM messages ORDER BY created_at DESC")
        rows = cursor.fetchall()

        messages = []
        for row in rows:
            try:
                content = json.loads(row["content"])
            except:
                content = {"message": row["content"]}
            messages.append({
                "message": content.get("message") or content.get("content"),
                "timestamp": content.get("timestamp") or str(row["created_at"])
            })

        return jsonify({"messages": messages}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
