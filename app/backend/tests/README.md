# Webhook Tests

This directory contains tests for the webhook functionality, with a particular focus on WhatsApp message handling.

## Running the Tests

To run the tests, use the following command from the project root directory:

```bash
python -m pytest app/backend/tests -v
```

## Available Test Cases

### Basic Webhook Tests
- `test_webhook_endpoint`: Tests the basic webhook endpoint with JSON payload
- `test_webhook_endpoint_invalid_payload`: Tests handling of invalid JSON payloads
- `test_status_callback_endpoint`: Tests the status callback endpoint
- `test_status_callback_invalid_payload`: Tests handling of invalid status callback payloads

### WhatsApp Message Tests
- `test_whatsapp_text_message`: Tests handling of a WhatsApp text message (RSVP intent)
- `test_whatsapp_greeting`: Tests handling of a greeting message ("שלום")
- `test_whatsapp_question`: Tests handling of a question message
- `test_whatsapp_with_media`: Tests handling of a message with media attachments
- `test_empty_webhook`: Tests handling of empty webhook payloads
- `test_raw_string_webhook`: Tests handling of raw string data

## Test Data

Test data fixtures are defined in `conftest.py`:

1. `test_whatsapp_text_message`: Example of a WhatsApp RSVP message
2. `test_whatsapp_greeting`: Example of a WhatsApp greeting
3. `test_whatsapp_question`: Example of a WhatsApp question
4. `test_whatsapp_with_media`: Example of a WhatsApp message with an image attachment

## Webhook Format

The tests simulate Twilio WhatsApp webhook messages using the `application/x-www-form-urlencoded` content type, matching the format of real Twilio webhook requests.

## Examples

### Example WhatsApp RSVP Message

```python
{
    "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "NumMedia": "0",
    "ProfileName": "Eyal",
    "MessageType": "text",
    "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "WaId": "972506228892",
    "SmsStatus": "received",
    "Body": "אישור הגעה",
    "To": "whatsapp:+972509518554",
    "MessagingServiceSid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "NumSegments": "1",
    "ReferralNumMedia": "0",
    "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "From": "whatsapp:+972506228892",
    "ApiVersion": "2010-04-01"
}
```

### Example WhatsApp Media Message

```python
{
    "SmsMessageSid": "MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "NumMedia": "1",
    "ProfileName": "מיכל",
    "MessageType": "text",
    "SmsSid": "MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "WaId": "9725054321123",
    "SmsStatus": "received",
    "Body": "",
    "To": "whatsapp:+972509518554",
    "MediaContentType0": "image/jpeg",
    "MediaUrl0": "https://example.com/api/2010-04-01/Accounts/ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/Messages/MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/Media/MExxxx",
    "MessagingServiceSid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "NumSegments": "1",
    "ReferralNumMedia": "0",
    "MessageSid": "MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "From": "whatsapp:+9725054321123",
    "ApiVersion": "2010-04-01"
}
``` 