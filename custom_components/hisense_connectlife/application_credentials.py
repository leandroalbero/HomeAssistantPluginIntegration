"""Application Credentials support for Hisense AC Plugin."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .const import CLIENT_ID, CLIENT_SECRET, OAUTH2_AUTHORIZE, OAUTH2_TOKEN
from .oauth2 import OAUTH2_CALLBACK_URL

_LOGGER = logging.getLogger(__name__)


async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: dict
) -> config_entry_oauth2_flow.LocalOAuth2Implementation:
    """Return auth implementation for a credential."""
    return HisenseOAuth2Implementation(hass)


class HisenseOAuth2Implementation(config_entry_oauth2_flow.LocalOAuth2Implementation):
    """Hisense OAuth2 implementation for Application Credentials."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize Hisense OAuth2 implementation."""
        super().__init__(
            hass=hass,
            domain="hisense_connectlife",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            authorize_url=OAUTH2_AUTHORIZE,
            token_url=OAUTH2_TOKEN,
        )

    @property
    def name(self) -> str:
        """Name of the implementation."""
        return "Hisense Air Conditioner"

    @property
    def redirect_uri(self) -> str:
        """Return the redirect URI."""
        return OAUTH2_CALLBACK_URL
