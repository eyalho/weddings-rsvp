import logging

logging.basicConfig(level=logging.INFO)

def handle_webhook(data: dict):
    # Logic to process incoming messages
    logging.info("Processing webhook data: %s", data)
    return {"status": "webhook processed"}

def handle_status_callback(data: dict):
    # Logic to process status updates
    logging.info("Processing status callback data: %s", data)
    return {"status": "status callback processed"}