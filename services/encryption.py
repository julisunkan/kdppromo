from cryptography.fernet import Fernet
import os

class EncryptionService:
    def __init__(self, key=None):
        if key is None:
            key = os.environ.get('APP_SECRET_KEY')
        if not key:
            raise ValueError("APP_SECRET_KEY environment variable not set")
        
        # Ensure key is bytes and valid for Fernet
        if isinstance(key, str):
            key = key.encode()
        
        # Fernet requires a 32-byte base64-encoded key. 
        # If the user provides a simple string, we might need to pad/hash it, 
        # but for now we assume they provide a valid Fernet key or we handle it.
        try:
            self.fernet = Fernet(key)
        except Exception:
            # If invalid, we'll try to generate a key from the string
            import hashlib
            import base64
            hashed = hashlib.sha256(key).digest()
            fernet_key = base64.urlsafe_b64encode(hashed)
            self.fernet = Fernet(fernet_key)

    def encrypt(self, text):
        if not text:
            return None
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text):
        if not encrypted_text:
            return None
        return self.fernet.decrypt(encrypted_text.encode()).decode()
