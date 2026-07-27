import base64
import json
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException
import binascii
from .signature import generate_signature
import hmac

# Encode the pagination cursor with a signature
def encode_cursor(created_at: datetime, cursor_id: UUID) -> str:

    # Create the cursor payload
    payload = {
        "created_at": created_at.isoformat(),
        "cursor_id": str(cursor_id),
    }

    # Convert the payload to JSON
    json_data = json.dumps(payload)

    # Encode the payload using URL-safe Base64
    encoded_payload=base64.urlsafe_b64encode(
        json_data.encode()
    ).decode()

    # Generate a signature for the encoded payload
    signature = generate_signature(encoded_payload)

    # Return the encoded payload and signature
    return f"{encoded_payload}.{signature}"



# Decode and validate a pagination cursor
def decode_cursor(cursor: str):
    try:

        # Split the encoded payload and signature
        encoded_payload, signature = cursor.rsplit(".", 1)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid cursor."
        )

    # Generate the expected signature
    expected_signature=generate_signature(encoded_payload)

    # Verify that the cursor has not been tampered with
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=400,
            detail="Invalid cursor."
        )

    try:

        # Decode the Base64 payload
        decoded = base64.urlsafe_b64decode(encoded_payload.encode()).decode()

        # Parse the JSON payload
        payload = json.loads(decoded)

        # Extract cursor fields
        created_at = payload.get("created_at")
        cursor_id = payload.get("cursor_id")

        # Ensure all required fields are present
        if created_at is None or cursor_id is None:
            raise ValueError

        # Return the decoded cursor values
        return (
            datetime.fromisoformat(created_at),
            UUID(cursor_id),
        )

    except (
        ValueError,
        TypeError,
        json.JSONDecodeError,
        binascii.Error,
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid cursor."
        )