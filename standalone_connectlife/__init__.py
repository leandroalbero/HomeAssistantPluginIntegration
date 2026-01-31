"""Standalone ConnectLife client for Hisense devices."""

from .api import ConnectLifeApiClient
from .oauth import OAuth2Session, TokenStorage
from .models import DeviceInfo
from .exceptions import (
    ConnectLifeError,
    AuthenticationError,
    TokenError,
    ApiError,
    DeviceError,
)
from . import config

__version__ = "1.0.0"
__all__ = [
    "ConnectLifeApiClient",
    "OAuth2Session",
    "TokenStorage",
    "DeviceInfo",
    "ConnectLifeError",
    "AuthenticationError",
    "TokenError",
    "ApiError",
    "DeviceError",
    "config",
]
