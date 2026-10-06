# app/core/encryption.py
from cryptography.fernet import Fernet
from app.config import settings

_cipher = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    return _cipher.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return _cipher.decrypt(token.encode()).decode()
