#!/usr/bin/env python3
r"""
ConnectLife CLI - Standalone client for Hisense ConnectLife devices.

This script uses the SAME OAuth2 redirect URL as Home Assistant:
http://homeassistant.local:8123/auth/external/callback

REQUIREMENT: You must add this line to your hosts file:
    127.0.0.1 homeassistant.local

On macOS/Linux: sudo nano /etc/hosts
On Windows: C:\Windows\System32\drivers\etc\hosts
"""

import argparse
import asyncio
import json
import logging
import os
import socket
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv

# Load .env file before importing our modules
env_paths = [
    Path(".env"),
    Path.home() / ".connectlife.env",
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break

from standalone_connectlife import (
    ConnectLifeApiClient,
    OAuth2Session,
    TokenStorage,
    DeviceInfo,
    AuthenticationError,
    TokenError,
    ApiError,
)
from standalone_connectlife.config import LOG_LEVEL, OAUTH2_CALLBACK_URL

# Set up logging
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOGGER = logging.getLogger(__name__)


def check_hosts_file() -> bool:
    """Check if homeassistant.local is configured in hosts file."""
    try:
        # Try to resolve homeassistant.local
        socket.gethostbyname("homeassistant.local")
        return True
    except socket.gaierror:
        return False


def print_hosts_instructions():
    """Print instructions for configuring hosts file."""
    print("\n" + "=" * 70)
    print("⚠️  HOSTS FILE CONFIGURATION REQUIRED")
    print("=" * 70)
    print("\nTo use this tool, you must add the following line to your hosts file:")
    print("\n    127.0.0.1 homeassistant.local")
    print("\nInstructions:")

    if sys.platform == "darwin":  # macOS
        print("\n  macOS:")
        print("    1. Open Terminal")
        print("    2. Run: sudo nano /etc/hosts")
        print("    3. Add the line: 127.0.0.1 homeassistant.local")
        print("    4. Save (Ctrl+O, Enter, Ctrl+X)")
        print("    5. Flush DNS: sudo killall -HUP mDNSResponder")

    elif sys.platform == "linux":
        print("\n  Linux:")
        print("    1. Open Terminal")
        print("    2. Run: sudo nano /etc/hosts")
        print("    3. Add the line: 127.0.0.1 homeassistant.local")
        print("    4. Save (Ctrl+O, Enter, Ctrl+X)")

    elif sys.platform == "win32":  # Windows
        print("\n  Windows:")
        print("    1. Open Notepad as Administrator")
        print("    2. Open: C:\\Windows\\System32\\drivers\\etc\\hosts")
        print("    3. Add the line: 127.0.0.1 homeassistant.local")
        print("    4. Save the file")
        print("    5. Open Command Prompt as Administrator")
        print("    6. Run: ipconfig /flushdns")

    print("\n" + "=" * 70)
    print("After adding the line, run this script again.")
    print("=" * 70 + "\n")


def print_table(headers: List[str], rows: List[List[Any]]) -> None:
    """Print data in a formatted table."""
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print("-" * len(header_line))

    for row in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))


def print_device_details(
    device: DeviceInfo, parsed_status: Optional[Dict] = None
) -> None:
    """Print detailed device information."""
    print(f"\n{'=' * 60}")
    print(f"Device: {device.name}")
    print(f"{'=' * 60}")
    print(f"  PUID: {device.puid}")
    print(f"  Device ID: {device.device_id}")
    print(f"  Type: {device.type_code}-{device.feature_code} ({device.type_name})")
    print(f"  Feature: {device.feature_name}")
    print(f"  Room: {device.room_name or 'N/A'}")
    print(f"  Online: {'Yes' if device.is_online else 'No'}")
    print(f"  Power: {'On' if device.is_onOff else 'Off'}")

    if parsed_status:
        print(f"\n  Status:")
        for key, value in parsed_status.items():
            print(f"    {key}: {value}")
    elif device.status:
        print(f"\n  Raw Status:")
        for key, value in device.status.items():
            print(f"    {key}: {value}")

    if device.failed_data:
        print(f"\n  Faults: {', '.join(device.failed_data)}")


async def authenticate_interactive(oauth_session: OAuth2Session) -> bool:
    """Interactive authentication flow."""
    auth_url = oauth_session.generate_authorize_url()

    print("\n" + "=" * 60)
    print("ConnectLife Authentication")
    print("=" * 60)
    print("\n1. Open this URL in your browser:")
    print(f"\n   {auth_url}\n")
    print("2. Log in with your ConnectLife account")
    print("3. After login, you'll see 'Page not found' or similar")
    print("4. Copy the FULL URL from your browser's address bar")
    print("   (It should start with: http://homeassistant.local:8123/...)")
    print("\n" + "-" * 60)

    # Get the full callback URL from user
    callback_url = input("\nPaste the full callback URL: ").strip()

    if not callback_url:
        print("Error: No URL provided")
        return False

    # Extract authorization code from URL
    try:
        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(callback_url)
        params = parse_qs(parsed.query)

        if "code" not in params:
            print("Error: No authorization code found in URL")
            print(f"URL received: {callback_url}")
            return False

        auth_code = params["code"][0]

    except Exception as e:
        print(f"Error parsing URL: {e}")
        return False

    try:
        # Exchange code for tokens
        token = await oauth_session.exchange_code(auth_code)
        print("\n✓ Authentication successful!")
        print(f"  Access token expires in {token.get('expires_in', 'unknown')} seconds")
        return True

    except AuthenticationError as e:
        print(f"\n✗ Authentication failed: {e}")
        return False


async def list_devices(
    api_client: ConnectLifeApiClient, json_output: bool = False
) -> None:
    """List all devices."""
    try:
        devices = await api_client.async_get_devices()

        if not devices:
            print("No devices found.")
            return

        if json_output:
            devices_dict = {
                device_id: {
                    **device.to_dict(),
                    "parsed_status": api_client.parse_device_status(device),
                }
                for device_id, device in devices.items()
            }
            print(json.dumps(devices_dict, indent=2))
        else:
            headers = ["Name", "Type", "Online", "Power", "Room"]
            rows = []

            for device in devices.values():
                parsed_status = api_client.parse_device_status(device)
                power = parsed_status.get(
                    "t_power", device.status.get("t_power", "Unknown")
                )

                rows.append(
                    [
                        device.name,
                        f"{device.type_code}-{device.feature_code}",
                        "Yes" if device.is_online else "No",
                        power,
                        device.room_name or "N/A",
                    ]
                )

            print(f"\nFound {len(devices)} device(s):\n")
            print_table(headers, rows)
            print()

    except ApiError as e:
        print(f"Error fetching devices: {e}")


async def show_device_status(
    api_client: ConnectLifeApiClient, puid: str, json_output: bool = False
) -> None:
    """Show detailed status for a specific device."""
    try:
        devices = await api_client.async_get_devices()

        device = None
        for d in devices.values():
            if d.puid == puid:
                device = d
                break

        if not device:
            print(f"Device with PUID '{puid}' not found")
            return

        parsed_status = api_client.parse_device_status(device)

        if json_output:
            print(
                json.dumps(
                    {"device": device.to_dict(), "parsed_status": parsed_status},
                    indent=2,
                )
            )
        else:
            print_device_details(device, parsed_status)

    except ApiError as e:
        print(f"Error fetching device status: {e}")


async def control_device(
    api_client: ConnectLifeApiClient, puid: str, properties: Dict[str, Any]
) -> None:
    """Send control commands to a device."""
    try:
        result = await api_client.async_control_device(puid, properties)

        if result.get("success"):
            print(f"✓ Command sent successfully")
            status = result.get("status", {})
            if status:
                print("  Updated properties:")
                for key, value in status.items():
                    print(f"    {key}: {value}")
        else:
            print(f"✗ Command failed")

    except ApiError as e:
        print(f"Error controlling device: {e}")


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ConnectLife CLI - Control Hisense smart devices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
REQUIREMENT: Hosts File Configuration
  You MUST add this line to your hosts file before using this tool:
      127.0.0.1 homeassistant.local

  macOS/Linux: sudo nano /etc/hosts
  Windows: C:\\Windows\\System32\\drivers\\etc\\hosts

Authentication:
  This tool uses the SAME OAuth2 redirect URL as Home Assistant.
  After adding the hosts file entry, run:
      python connectlife_cli.py --list-devices

  Then:
  1. Open the generated URL in your browser
  2. Log in with your ConnectLife account
  3. Copy the FULL callback URL (starts with homeassistant.local)
  4. Paste it back into the terminal

Examples:
  # Setup (add to hosts file first!)
  echo "127.0.0.1 homeassistant.local" | sudo tee -a /etc/hosts

  # List devices
  python connectlife_cli.py --list-devices

  # Show device status
  python connectlife_cli.py --device <PUID> --status

  # Turn on a device
  python connectlife_cli.py --device <PUID> --set-property t_power=1

  # Logout
  python connectlife_cli.py --logout
        """,
    )

    parser.add_argument(
        "--list-devices", "-l", action="store_true", help="List all devices"
    )
    parser.add_argument("--device", "-d", metavar="PUID", help="Device PUID to control")
    parser.add_argument(
        "--status", "-s", action="store_true", help="Show device status"
    )
    parser.add_argument(
        "--set-property",
        action="append",
        metavar="KEY=VALUE",
        help="Set a device property (can be used multiple times)",
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--logout", action="store_true", help="Logout and clear stored credentials"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.logout:
        storage = TokenStorage()
        storage.clear()
        print("✓ Logged out successfully. Credentials cleared.")
        return

    if not args.list_devices and not args.device:
        # Check hosts file before showing help
        if not check_hosts_file():
            print_hosts_instructions()
            return
        parser.print_help()
        return

    if args.device and not (args.status or args.set_property):
        print("Error: --device requires --status or --set-property")
        parser.print_help()
        return

    # Check hosts file configuration
    if not check_hosts_file():
        print_hosts_instructions()
        sys.exit(1)

    print("✓ Hosts file configured correctly (homeassistant.local -> 127.0.0.1)")

    async with aiohttp.ClientSession() as session:
        oauth_session = OAuth2Session(session)

        if not oauth_session.is_authenticated():
            print("No valid credentials found. Starting authentication...")
            success = await authenticate_interactive(oauth_session)
            if not success:
                sys.exit(1)
        else:
            print("✓ Using existing credentials")

        api_client = ConnectLifeApiClient(session, oauth_session)

        try:
            if args.list_devices:
                await list_devices(api_client, args.json)

            if args.device:
                if args.status:
                    await show_device_status(api_client, args.device, args.json)

                if args.set_property:
                    properties = {}
                    for prop in args.set_property:
                        if "=" not in prop:
                            print(
                                f"Error: Invalid property format '{prop}'. Use KEY=VALUE"
                            )
                            sys.exit(1)
                        key, value = prop.split("=", 1)
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                pass
                        properties[key] = value

                    await control_device(api_client, args.device, properties)

        except TokenError as e:
            print(f"Authentication error: {e}")
            print("Please run again to re-authenticate.")
            oauth_session.logout()
            sys.exit(1)
        except ApiError as e:
            print(f"API error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
