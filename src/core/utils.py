from hashlib import sha256

def get_note_id(text: str, salt: str) -> str:
    return sha256(
        text.encode("UTF-8") + salt.encode("UTF-8")
    ).hexdigest()
