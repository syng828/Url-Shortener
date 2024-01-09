import base64
import hashlib
import secrets


def create_alias(url: str):
    seed = secrets.token_bytes(16)  # generates a random 16-byte value
    # adds to url to ensure its unique
    data_to_hash = seed + url.encode('utf-8')
    hasher = hashlib.sha256(data_to_hash)
    hash_bytes = hasher.digest()
    alias = base64.urlsafe_b64encode(
        hash_bytes).decode('utf-8')[:5]
    return alias
