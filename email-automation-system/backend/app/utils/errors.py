from fastapi import HTTPException, status


class AppException(Exception):
    """Base application exception."""
    pass


class AuthenticationException(AppException):
    """Raised when authentication fails."""
    pass


class AuthorizationException(AppException):
    """Raised when user is not authorized."""
    pass


class InvalidTokenException(AuthenticationException):
    """Raised when JWT token is invalid."""
    pass


class GmailAPIException(AppException):
    """Raised when Gmail API request fails."""
    pass


class EmailProcessingException(AppException):
    """Raised when email processing fails."""
    pass


class OpenAIException(AppException):
    """Raised when OpenAI API request fails."""
    pass


def unauthorized_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden_exception():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this resource",
    )


def not_found_exception(resource: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found",
    )
