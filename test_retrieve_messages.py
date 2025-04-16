import requests
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

try:
    response = requests.get("http://127.0.0.1:5001/messages")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Expected a list of messages"

    # Optional: Validate structure of the first message
    if data:
        sample = data[0]
        assert 'transaction_number' in sample, "Missing transaction_number"
        assert 'timestamp' in sample, "Missing timestamp"

    print("Test Passed: API endpoint returned messages correctly.")

except Exception as e:
    logging.error(f"Test Failed: {str(e)}")
