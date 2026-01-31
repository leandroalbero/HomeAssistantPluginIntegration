"""Configuration module for ConnectLife client."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(".env")
if env_path.exists():
    load_dotenv(env_path)

# Load from ~/.env if local .env doesn't exist
home_env_path = Path.home() / ".connectlife.env"
if not env_path.exists() and home_env_path.exists():
    load_dotenv(home_env_path)

# OAuth2 Configuration
CLIENT_ID = os.getenv("CONNECTLIFE_CLIENT_ID", "9793620883275788")
CLIENT_SECRET = os.getenv(
    "CONNECTLIFE_CLIENT_SECRET",
    "7h1m3gZVlILyBvIFBNmzXwoFYLhkGqG9NQd2jBzuZCqJKCTyCtYwQtXi4tVBjg9B",
)

# Use Home Assistant redirect URL to match the integration
OAUTH2_CALLBACK_URL = os.getenv(
    "CONNECTLIFE_CALLBACK_URL", "http://homeassistant.local:8123/auth/external/callback"
)

# Token Storage
TOKEN_FILE = os.getenv("CONNECTLIFE_TOKEN_FILE", "~/.connectlife_tokens.json")

# API Configuration
ENV = os.getenv("CONNECTLIFE_ENV", "production")

if ENV == "test":
    OAUTH2_AUTHORIZE = (
        os.getenv("CONNECTLIFE_OAUTH_URL", "https://test-oauth.hijuconn.com") + "/login"
    )
    OAUTH2_TOKEN = (
        os.getenv("CONNECTLIFE_OAUTH_URL", "https://test-oauth.hijuconn.com")
        + "/oauth/token"
    )
    API_BASE_URL = os.getenv(
        "CONNECTLIFE_API_BASE_URL", "https://test-juapi-3rd.hijuconn.com"
    )
    WEBSOCKET_URL = (
        os.getenv("CONNECTLIFE_WS_URL", "wss://test-clife-eu-gateway.hijuconn.com")
        + "/msg/get_msg_and_channels"
    )
else:
    OAUTH2_AUTHORIZE = (
        os.getenv("CONNECTLIFE_OAUTH_URL", "https://oauth.hijuconn.com") + "/login"
    )
    OAUTH2_TOKEN = (
        os.getenv("CONNECTLIFE_OAUTH_URL", "https://oauth.hijuconn.com")
        + "/oauth/token"
    )
    API_BASE_URL = os.getenv(
        "CONNECTLIFE_API_BASE_URL", "https://juapi-3rd.hijuconn.com"
    )
    WEBSOCKET_URL = (
        os.getenv("CONNECTLIFE_WS_URL", "wss://clife-eu-gateway.hijuconn.com")
        + "/msg/get_msg_and_channels"
    )

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
