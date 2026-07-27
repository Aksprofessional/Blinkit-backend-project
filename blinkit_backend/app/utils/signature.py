import hashlib
import hmac
from app.core.config import Setting

# Generate an HMAC-SHA256 signature for the provided payload
def generate_signature(payload: str) -> str:

    # Create and return the hexadecimal signature
    return hmac.new(
        Setting.SECRET_KEY_CURSOR.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()