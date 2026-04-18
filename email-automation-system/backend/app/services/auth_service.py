from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import get_settings
from app.utils.errors import AuthenticationException, InvalidTokenException
from app.utils.crypto import get_token_encryption
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for JWT token and password operations."""

    @staticmethod
    def create_access_token(user_id: str, expires_delta: timedelta = None) -> str:
        """Create JWT access token."""
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.jwt_expiration_minutes)

        expire = datetime.utcnow() + expires_delta
        to_encode = {"sub": user_id, "exp": expire}

        try:
            encoded_jwt = jwt.encode(
                to_encode,
                settings.jwt_secret_key,
                algorithm=settings.jwt_algorithm,
            )
            return encoded_jwt
        except Exception as e:
            logger.error(f"Failed to create JWT token: {e}")
            raise AuthenticationException("Failed to create token")

    @staticmethod
    def verify_token(token: str) -> str:
        """Verify JWT token and return user_id."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise InvalidTokenException("Token missing user_id")
            return user_id
        except JWTError as e:
            logger.error(f"Invalid JWT token: {e}")
            raise InvalidTokenException(f"Invalid token: {e}")

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)


class OAuthService:
    """Service for OAuth token management."""

    def __init__(self):
        self.encryption = get_token_encryption()

    def encrypt_token(self, token: str) -> str:
        """Encrypt sensitive token for storage."""
        try:
            return self.encryption.encrypt(token)
        except Exception as e:
            logger.error(f"Failed to encrypt token: {e}")
            raise AuthenticationException("Failed to encrypt token")

    def decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt token from storage."""
        try:
            return self.encryption.decrypt(encrypted_token)
        except Exception as e:
            logger.error(f"Failed to decrypt token: {e}")
            raise AuthenticationException("Failed to decrypt token")

    @staticmethod
    def is_token_expiring(expiry: datetime, hours_ahead: int = 1) -> bool:
        """Check if token is expiring soon."""
        return datetime.utcnow() + timedelta(hours=hours_ahead) > expiry
