import base64
import hashlib


def create_alias(url: str):
    url_bytes = url.encode('utf-8')
    hasher = hashlib.sha256(url_bytes)
    hash_bytes = hasher.digest()
    alias = base64.urlsafe_b64encode(
        hash_bytes).decode('utf-8').rstrip('=')[:5]
    return alias


print(create_alias("https://youtube.com"))
print(create_alias("https://google.com"))
