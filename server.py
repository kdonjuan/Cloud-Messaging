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
    publisher


