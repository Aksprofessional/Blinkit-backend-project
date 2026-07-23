import base64
import json
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException
import binascii
from .signature import generate_signature
import hmac

def encode_cursor(created_at: datetime, cursor_id: UUID) -> str:

    payload = {
        "created_at": created_at.isoformat(),
        "cursor_id": str(cursor_id),
    }

    json_data = json.dumps(payload)

    encoded_payload=base64.urlsafe_b64encode(
        json_data.encode()
    ).decode()

    signature = generate_signature(encoded_payload)

    return f"{encoded_payload}.{signature}"



def decode_cursor(cursor: str):
    try:
        encoded_payload, signature = cursor.rsplit(".", 1)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid cursor."
        )
    expected_signature=generate_signature(encoded_payload)
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=400,
            detail="Invalid cursor."
        )

    try:
        decoded = base64.urlsafe_b64decode(encoded_payload.encode()).decode()

        payload = json.loads(decoded)

        created_at = payload.get("created_at")
        cursor_id = payload.get("cursor_id")

        if created_at is None or cursor_id is None:
            raise ValueError

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