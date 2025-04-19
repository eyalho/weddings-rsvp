# Test Credential Guidelines

## Why This Matters

GitHub and other platforms use secret scanning to prevent accidental leakage of real credentials. This is good for security, but can lead to false positives when using realistic-looking test data.

## Guidelines for Test Credentials

1. **Never use real API keys or credentials** in tests, documentation, or examples, even if they're expired or revoked.

2. **Use standardized fake values** for all credentials in test fixtures:
   - For Twilio SIDs: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (prefix + 32 x's)
   - For Twilio Auth Tokens: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (32 x's)
   - For Message SIDs: `SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (prefix + 32 x's)
   - For Media SIDs: `MExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (prefix + 32 x's)

3. **Use fake domains** like `example.com` for all URLs, never real API endpoints with real-looking credentials.

4. **Avoid patterns that look like real secrets**, such as:
   - Hash-like strings (e.g., long hexadecimal strings)
   - Base64-encoded content that is 32+ characters long
   - Strings with prefixes that match real credential patterns (SK_, pk_live_, etc.)

5. **Use environment variables** for real credentials in actual code, never hardcode them.

## Example Fixtures

Good example of a Twilio webhook test fixture:

```python
{
    "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "NumMedia": "0",
    "ProfileName": "Example User",
    "MessageType": "text",
    "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", 
    "WaId": "1234567890",
    "SmsStatus": "received",
    "Body": "Test message",
    "To": "whatsapp:+1234567890",
    "MessagingServiceSid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "From": "whatsapp:+0987654321", 
    "ApiVersion": "2010-04-01"
}
```

## Testing with Real Credentials

For integration tests that need real credentials:

1. Use environment variables loaded from `.env` files that are in `.gitignore`
2. Use mock services for testing where possible
3. Consider using separate test accounts with limited permissions 