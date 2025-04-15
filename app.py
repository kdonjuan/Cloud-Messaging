from flask import Flask, jsonify
import datetime

app = Flask(__name__)

# Simulated message store (in a real case, this would be replaced with DB or Pub/Sub data)
MESSAGES = [
    {
        "item_id": "12345",
        "location": "Warehouse A",
        "quantity": 10,
        "transaction_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transaction_number": "TXN001"
    },
    {
        "item_id": "67890",
        "location": "Warehouse B",
        "quantity": 5,
        "transaction_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transaction_number": "TXN002"
    }
]

@app.route("/api/messages")
def get_messages():
    return jsonify(MESSAGES)

if __name__ == "__main__":
    app.run(debug=True)
