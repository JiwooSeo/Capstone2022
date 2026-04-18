from cryptography.fernet import Fernet
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class TokenEncryption:
    """Handles encryption and decryption of sensitive tokens."""

    def __init__(self, key: str):
        try:
            self.cipher = Fernet(key.encode())
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            raise

    @staticmethod
    def generate_key() -> str:
        """Generate a new Fernet key."""
        return Fernet.generate_key().decode()

    def encrypt(self, data: str) -> str:
        """Encrypt data."""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data."""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise


def get_token_encryption() -> TokenEncryption:
    """Get token encryption instance."""
    return TokenEncryption(settings.encryption_key)
