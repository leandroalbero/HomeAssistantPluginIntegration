"""Custom exceptions for ConnectLife client."""


class ConnectLifeError(Exception):
    """Base exception for ConnectLife client."""

    pass


class AuthenticationError(ConnectLifeError):
    """Raised when authentication fails."""

    pass


class TokenError(ConnectLifeError):
    """Raised when token is invalid or expired."""

    pass


class ApiError(ConnectLifeError):
    """Raised when API request fails."""

    pass


class DeviceError(ConnectLifeError):
    """Raised when device operation fails."""

    pass
