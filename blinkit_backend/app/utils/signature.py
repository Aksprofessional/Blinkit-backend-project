import base64
import hashlib
import hmac
import json
from datetime import datetime
from uuid import UUID
from app.core.config import Setting

def generate_signature(payload: str) -> str:
    return hmac.new(
        Setting.SECRET_KEY_CURSOR.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()