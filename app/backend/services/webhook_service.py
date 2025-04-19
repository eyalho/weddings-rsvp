import logging
import json
import sys
from pprint import pformat

# Don't configure logging here, use the configuration from main.py
# logging.basicConfig() calls should only happen once in the application
logger = logging.getLogger(__name__)

def handle_webhook(data: dict):
    # Logic to process incoming messages
    logger.warning("Processing webhook data: %s", data)
    
    # Add verbose debugging output (using warning level to ensure it's printed)
    logger.warning("Webhook payload details:")
    logger.warning("=" * 50)
    logger.warning("Content type: %s", type(data))
    logger.warning("Content structure:\n%s", pformat(data, indent=2))
    
    try:
        # Pretty print the JSON for better readability in logs
        pretty_json = json.dumps(data, indent=2, sort_keys=True)
        logger.warning("Full webhook content:\n%s", pretty_json)
    except Exception as e:
        logger.error("Error printing webhook content: %s", str(e))
    
    logger.warning("=" * 50)
    
    return {"status": "webhook processed"}

def handle_status_callback(data: dict):
    # Logic to process status updates
    logger.warning("Processing status callback data: %s", data)
    return {"status": "status callback processed"}