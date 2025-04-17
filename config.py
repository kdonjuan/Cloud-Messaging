import os

PROJECT_ID = "marine-actor-450915-b0"
SUBSCRIPTION_ID = "message-subscription"
TOPIC_ID = "message-topic"

INSTANCE_CONNECTION_NAME = "marine-actor-450915-b0:us-central1:is-capstone"
DB_NAME = "iscapstone_db"
DB_USER = "test_user1"
DB_PASSWORD = "is-capstone"

# Load this from the environment
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
