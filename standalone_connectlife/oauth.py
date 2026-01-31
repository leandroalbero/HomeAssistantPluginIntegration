"""OAuth2 implementation for standalone ConnectLife client."""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Optional

import aiohttp

from .const import (
    CLIENT_ID,
    CLIENT_SECRET,
    OAUTH2_AUTHORIZE,
    OAUTH2_CALLBACK_URL,
    OAUTH2_TOKEN,
    TOKEN_FILE,
)
from .exceptions import AuthenticationError, TokenError

_LOGGER = logging.getLogger(__name__)


class TokenStorage:
    """Handles token storage and retrieval."""

    def __init__(self, token_file: str = TOKEN_FILE):
        """Initialize token storage."""
        self.token_path = Path(token_file).expanduser()

    def load(self) -> Optional[Dict[str, Any]]:
        """Load tokens from file."""
        try:
            if self.token_path.exists():
                with open(self.token_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            _LOGGER.warning("Failed to load tokens: %s", e)
        return None

    def save(self, token: Dict[str, Any]) -> None:
        """Save tokens to file."""
        try:
            self.token_path.parent.mkdir(parents=True, exist_ok=True)
            # Set restrictive permissions (user read/write only)
            with open(self.token_path, "w") as f:
                json.dump(token, f, indent=2)
            os.chmod(self.token_path, 0o600)
            _LOGGER.debug("Tokens saved to %s", self.token_path)
        except Exception as e:
            _LOGGER.error("Failed to save tokens: %s", e)

    def clear(self) -> None:
        """Clear stored tokens."""
        try:
            if self.token_path.exists():
                self.token_path.unlink()
                _LOGGER.debug("Tokens cleared")
        except Exception as e:
            _LOGGER.error("Failed to clear tokens: %s", e)


class OAuth2Session:
    """OAuth2 session handler for standalone use."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize OAuth2 session."""
        self.session = session
        self.token = token or {}
        self.token_storage = TokenStorage()

        # Load existing tokens if not provided
        if not self.token:
            self.token = self.token_storage.load() or {}

        _LOGGER.debug("Initialized OAuth2Session")

    async def async_ensure_token_valid(self) -> None:
        """Ensure that the token is valid."""
        if not self.token:
            _LOGGER.error("No token available")
            raise TokenError("No token available. Please authenticate first.")

        if self._is_token_expired():
            _LOGGER.debug("Token has expired, refreshing...")
            try:
                token_data = await self._refresh_token()
                self.token.update(token_data)
                self.token_storage.save(self.token)
                _LOGGER.debug("Token refreshed successfully")
            except Exception as e:
                _LOGGER.error("Failed to refresh token: %s", e)
                raise TokenError(f"Failed to refresh token: {e}")

    def _is_token_expired(self) -> bool:
        """Check if token is expired."""
        expires_at = self.token.get("expires_at")
        if not expires_at:
            expires_in = self.token.get("expires_in", 0)
            if expires_in:
                self.token["expires_at"] = time.time() + expires_in
                return False
            return True
        return time.time() >= expires_at - 300  # Refresh 5 minutes before expiry

    async def async_get_access_token(self) -> str:
        """Get the access token."""
        await self.async_ensure_token_valid()
        return self.token["access_token"]

    async def _refresh_token(self) -> Dict[str, Any]:
        """Refresh tokens."""
        refresh_token = self.token.get("refresh_token")
        if not refresh_token:
            raise TokenError("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
        }

        return await self._token_request(data)

    async def _token_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a token request."""
        _LOGGER.debug("Making token request to %s", OAUTH2_TOKEN)

        async with self.session.post(
            OAUTH2_TOKEN,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ) as resp:
            response = await resp.json()

            # Check for OAuth2 errors
            if "error" in response:
                error = response.get("error", "Unknown error")
                error_desc = response.get("error_description", "No details provided")
                raise AuthenticationError(
                    f"Authentication failed: {error} - {error_desc}"
                )

            # Check for API errors (resultCode field)
            if response.get("resultCode", 0) != 0:
                error = response.get("error", "Unknown error")
                error_desc = response.get("error_description", "No details provided")
                raise AuthenticationError(
                    f"Authentication failed: {error} - {error_desc}"
                )

            # Check for HTTP errors
            if resp.status != 200:
                text = await resp.text()
                raise AuthenticationError(
                    f"Token request failed: {resp.status} - {text}"
                )

            # Validate that we have the required token fields
            if "access_token" not in response:
                raise AuthenticationError("Invalid response: access_token not found")

            # Add expires_at to the token response
            if "expires_in" in response and "expires_at" not in response:
                response["expires_at"] = time.time() + response["expires_in"]

            return response

    async def exchange_code(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for tokens."""
        data = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": OAUTH2_CALLBACK_URL,
        }

        token = await self._token_request(data)
        self.token = token
        self.token_storage.save(token)
        return token

    async def login_with_password(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate with username and password using password grant.

        This uses the OAuth2 password grant flow to obtain tokens directly
        from email/password credentials.

        Args:
            username: Email address or username
            password: Account password

        Returns:
            Token dictionary containing access_token, refresh_token, etc.

        Raises:
            AuthenticationError: If authentication fails
        """
        _LOGGER.debug("Authenticating with password grant for user: %s", username)

        data = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": username,
            "password": password,
            "scope": "all",
        }

        try:
            token = await self._token_request(data)
            self.token = token
            self.token_storage.save(token)
            _LOGGER.info("Password authentication successful for user: %s", username)
            return token
        except AuthenticationError as e:
            _LOGGER.error("Password authentication failed: %s", e)
            raise AuthenticationError(
                f"Login failed. Please check your email and password."
            ) from e

    def generate_authorize_url(self) -> str:
        """Generate authorization URL."""
        params = {
            "client_id": CLIENT_ID,
            "redirect_uri": OAUTH2_CALLBACK_URL,
            "response_type": "code",
            "scope": "all",
        }

        query_string = urllib.parse.urlencode(params)
        return f"{OAUTH2_AUTHORIZE}?{query_string}"

    def is_authenticated(self) -> bool:
        """Check if we have valid tokens."""
        return bool(self.token.get("access_token"))

    def logout(self) -> None:
        """Clear all tokens."""
        self.token = {}
        self.token_storage.clear()
