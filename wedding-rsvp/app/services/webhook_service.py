def handle_webhook(data: dict):
    # Logic to process incoming messages
    print("Processing webhook data:", data)
    return {"status": "webhook processed"}

def handle_status_callback(data: dict):
    # Logic to process status updates
    print("Processing status callback data:", data)
    return {"status": "status callback processed"}