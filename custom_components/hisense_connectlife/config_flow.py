"""Config flow for Hisense AC Plugin integration."""

from __future__ import annotations

import logging
import time
from typing import Any
import urllib.parse

import voluptuous as vol

from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_NAME
from homeassistant.config_entries import ConfigEntry, OptionsFlow

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN, CLIENT_ID, CLIENT_SECRET
from .oauth2 import HisenseOAuth2Implementation, OAUTH2_CALLBACK_URL, get_redirect_url

_LOGGER = logging.getLogger(__name__)


class HisenseOptionsFlowHandler(OptionsFlow):
    """Handle Hisense AC options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        errors = {}
        description_placeholders = {"message": ""}  # Initialize with empty message

        if user_input is not None:
            coordinator = self.hass.data[DOMAIN][self.config_entry.entry_id]

            if user_input.get("refresh_devices", False):
                try:
                    # 重新获取设备列表
                    devices = await coordinator.api_client.async_get_devices
                    coordinator._devices = devices
                    # 强制更新一次状态
                    await coordinator.async_refresh()
                    description_placeholders["message"] = (
                        "Device list has been refreshed"
                    )
                except Exception as err:
                    _LOGGER.error("Failed to refresh device list: %s", err)
                    errors["base"] = "refresh_failed"

            if user_input.get("refresh_token", False):
                try:
                    # Record token before refresh
                    old_token = coordinator.api_client.oauth_session.token.get(
                        "access_token", ""
                    )[-10:]
                    _LOGGER.debug("Token before refresh: ...%s", old_token)

                    # Force token refresh
                    _LOGGER.debug("Forcing token refresh...")
                    token_data = coordinator.api_client.oauth_session.token

                    # Use our own OAuth2 implementation to refresh token
                    implementation = HisenseOAuth2Implementation(self.hass)
                    new_token = await implementation.async_refresh_token(token_data)

                    if new_token:
                        _LOGGER.debug(
                            "Token after refresh: ...%s",
                            new_token.get("access_token", "")[-10:],
                        )
                        # Update token in coordinator
                        coordinator.api_client.oauth_session.token = new_token
                        # Force update config entry data
                        self.hass.config_entries.async_update_entry(
                            self.config_entry,
                            data={**self.config_entry.data, "token": new_token},
                        )
                        _LOGGER.info("Token refreshed successfully")
                        description_placeholders["message"] = "Token has been refreshed"
                    else:
                        _LOGGER.warning("No new token received after refresh")
                        errors["base"] = "token_refresh_failed"
                except Exception as err:
                    _LOGGER.error("Failed to refresh token: %s", err)
                    errors["base"] = "token_refresh_failed"

            if not errors:
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self._get_options_schema(),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    def _get_options_schema(self) -> vol.Schema:
        """Get options schema."""
        return vol.Schema(
            {
                vol.Optional("refresh_devices", default=False): bool,
                vol.Optional("refresh_token", default=False): bool,
            }
        )


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler,
    domain=DOMAIN,
):
    """Config flow to handle Hisense AC Plugin OAuth2 authentication."""

    DOMAIN = DOMAIN
    VERSION = 1

    def __init__(self) -> None:
        """Initialize the flow."""
        super().__init__()
        self._flow_impl: HisenseOAuth2Implementation | None = None

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return _LOGGER

    @property
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow start."""
        _LOGGER.debug("Starting user step with input: %s", user_input)

        await self.async_set_unique_id(DOMAIN)

        if self._async_current_entries():
            _LOGGER.debug("Aborting due to single instance allowed")
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            # Show initial form with choice between automatic and manual auth
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("auth_method", default="manual"): vol.In(
                            {
                                "manual": "Manual (copy callback URL)",
                                "auto": "Automatic (requires homeassistant.local to resolve)",
                            }
                        ),
                    }
                ),
                description_placeholders={
                    "oauth_callback_url": get_redirect_url(self.hass),
                    "app_name": "Hisense AC",
                    "app_id": CLIENT_ID,
                },
            )

        auth_method = user_input.get("auth_method", "manual")

        if auth_method == "auto":
            # User has chosen automatic OAuth flow
            self._flow_impl = HisenseOAuth2Implementation(self.hass)
            self.flow_impl = self._flow_impl

            try:
                url = await self._flow_impl.async_generate_authorize_url(self.flow_id)
                _LOGGER.debug("Generated authorization URL: %s", url)
                return self.async_external_step(step_id="auth", url=url)
            except Exception as err:
                _LOGGER.error("Failed to generate authorize URL: %s", err)
                return self.async_abort(reason="authorize_url_fail")
        else:
            # User has chosen manual authentication
            return await self.async_step_manual_auth()

    async def async_step_manual_auth(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle manual authentication by pasting callback URL."""
        errors = {}

        if user_input is not None:
            callback_url = user_input.get("callback_url", "").strip()

            if not callback_url:
                errors["callback_url"] = "required"
            else:
                # Parse the callback URL to extract code
                try:
                    parsed = urllib.parse.urlparse(callback_url)
                    params = urllib.parse.parse_qs(parsed.query)

                    if "code" not in params:
                        errors["callback_url"] = "no_code"
                    else:
                        auth_code = params["code"][0]

                        _LOGGER.debug("Extracted auth code: %s...", auth_code[:10])

                        # Initialize OAuth implementation
                        self._flow_impl = HisenseOAuth2Implementation(self.hass)
                        self.flow_impl = self._flow_impl

                        # Exchange code for token directly
                        try:
                            import aiohttp
                            from .const import OAUTH2_TOKEN, CLIENT_ID, CLIENT_SECRET

                            token_data = {
                                "grant_type": "authorization_code",
                                "client_id": CLIENT_ID,
                                "client_secret": CLIENT_SECRET,
                                "code": auth_code,
                                "redirect_uri": OAUTH2_CALLBACK_URL,
                            }

                            _LOGGER.debug("Exchanging code for token...")

                            async with aiohttp.ClientSession() as session:
                                async with session.post(
                                    OAUTH2_TOKEN,
                                    data=token_data,
                                    headers={
                                        "Content-Type": "application/x-www-form-urlencoded"
                                    },
                                ) as resp:
                                    if resp.status != 200:
                                        text = await resp.text()
                                        _LOGGER.error(
                                            "Token request failed: %s - %s",
                                            resp.status,
                                            text,
                                        )
                                        errors["callback_url"] = "token_exchange_failed"
                                    else:
                                        token = await resp.json()

                                        # Check for OAuth errors
                                        if "error" in token:
                                            _LOGGER.error(
                                                "OAuth error: %s",
                                                token.get(
                                                    "error_description", token["error"]
                                                ),
                                            )
                                            errors["callback_url"] = (
                                                "token_exchange_failed"
                                            )
                                        else:
                                            _LOGGER.debug("Successfully obtained token")

                                            # Create the config entry
                                            return self.async_create_entry(
                                                title=self._flow_impl.name,
                                                data={
                                                    "token": token,
                                                    "auth_implementation": DOMAIN,
                                                    "implementation": DOMAIN,
                                                },
                                            )
                        except Exception as err:
                            _LOGGER.error("Failed to exchange code for token: %s", err)
                            errors["callback_url"] = "token_exchange_failed"

                except Exception as err:
                    _LOGGER.error("Failed to parse callback URL: %s", err)
                    errors["callback_url"] = "invalid_url"

        # Generate auth URL to show to user
        try:
            self._flow_impl = HisenseOAuth2Implementation(self.hass)
            auth_url = await self._flow_impl.async_generate_authorize_url(self.flow_id)
        except Exception as err:
            _LOGGER.error("Failed to generate auth URL: %s", err)
            auth_url = "Error generating URL"

        return self.async_show_form(
            step_id="manual_auth",
            data_schema=vol.Schema(
                {
                    vol.Required("callback_url", default=""): str,
                }
            ),
            description_placeholders={
                "auth_url": auth_url,
            },
            errors=errors,
        )

    async def async_step_auth(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the external auth step (automatic flow)."""
        _LOGGER.debug("Starting auth step with user_input: %s", user_input)
        return await super().async_step_auth(user_input)

    async def async_step_creation(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle creation step."""
        _LOGGER.debug("Starting creation step with user_input: %s", user_input)
        return await super().async_step_creation(user_input)

    async def async_oauth_create_entry(self, data: dict) -> FlowResult:
        """Create an entry for the flow."""
        _LOGGER.debug(
            "Creating entry with data: %s",
            {k: "***" if k in ("token", "token_type") else v for k, v in data.items()},
        )

        return self.async_create_entry(
            title=self.flow_impl.name,
            data={
                **data,
                "auth_implementation": DOMAIN,
                "implementation": DOMAIN,
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> HisenseOptionsFlowHandler:
        """Get the options flow for this handler."""
        return HisenseOptionsFlowHandler(config_entry)
