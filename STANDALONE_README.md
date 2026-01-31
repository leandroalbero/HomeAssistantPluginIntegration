# ConnectLife Standalone Client

A standalone Python client for controlling Hisense ConnectLife smart devices without Home Assistant.

## ⚠️ IMPORTANT: Hosts File Configuration Required

This tool uses the **same OAuth2 redirect URL as Home Assistant**. You MUST configure your hosts file first:

### Setup (One-time)

**Add this line to your hosts file:**
```
127.0.0.1 homeassistant.local
```

**macOS/Linux:**
```bash
sudo nano /etc/hosts
# Add: 127.0.0.1 homeassistant.local
# Save and exit
sudo killall -HUP mDNSResponder  # Flush DNS
```

**Windows:**
1. Open Notepad as Administrator
2. Open: `C:\Windows\System32\drivers\etc\hosts`
3. Add: `127.0.0.1 homeassistant.local`
4. Save the file
5. Run in Command Prompt (as Admin): `ipconfig /flushdns`

## Features

- 🔐 OAuth2 authentication (same as Home Assistant)
- 📱 List all your ConnectLife devices
- 📊 View detailed device status and properties
- 🎛️ Control devices (power, temperature, mode, etc.)
- 🏠 Support for multiple device types:
  - Split Air Conditioners (009)
  - Window Air Conditioners (008)
  - Portable Air Conditioners (006)
  - Dehumidifiers (007)
  - Heat Pumps (035)
- 📈 Power consumption monitoring
- 🔧 Fault detection and reporting

## Installation

1. Clone or download this repository
2. **Configure your hosts file** (see above)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### First Run - Authentication

```bash
python connectlife_cli.py --list-devices
```

You will see:
1. ✅ Hosts file check
2. 🌐 A URL to open in your browser
3. 🔑 Instructions to log in and paste the callback URL

**Steps:**
1. Open the generated URL in your browser
2. Log in with your ConnectLife account credentials
3. After login, you'll be redirected to `http://homeassistant.local:8123/...`
4. Copy the **full URL** from your browser's address bar
5. Paste it back into the terminal

Tokens are stored securely in `~/.connectlife_tokens.json` for future use.

### List All Devices

```bash
python connectlife_cli.py --list-devices
```

### View Device Status

```bash
python connectlife_cli.py --device <PUID> --status
```

### Control Devices

```bash
# Turn on
python connectlife_cli.py --device <PUID> --set-property t_power=1

# Turn off
python connectlife_cli.py --device <PUID> --set-property t_power=0

# Set temperature
python connectlife_cli.py --device <PUID> --set-property t_temp=24
```

## Why This Setup?

The ConnectLife OAuth2 client is configured to redirect to `homeassistant.local:8123`. This is the same redirect URL used by the official Home Assistant integration.

To use this standalone client, we need to:
1. Make `homeassistant.local` resolve to your local machine (`127.0.0.1`)
2. Capture the OAuth2 callback from the browser
3. Exchange the authorization code for tokens

This ensures compatibility with the official ConnectLife OAuth2 configuration.

## Troubleshooting

### "Hosts file not configured" error

Run the setup commands in the "⚠️ IMPORTANT" section above.

### "Wrong email or password" on web login

If you can log in to the ConnectLife mobile app but not the web OAuth page:
1. Make sure you're using the **same** email/password
2. Try clearing your browser cookies
3. Try in an incognito/private window
4. The mobile app might use a different authentication endpoint

### "Page not found" after login

This is **expected**! The OAuth2 flow redirects to `homeassistant.local`, which won't load a real page. That's why you need to copy the URL from the address bar.

### Callback URL issues

Make sure you copy the **full URL** including `http://homeassistant.local:8123/auth/external/callback?code=...`

## Configuration

Create a `.env` file for customization:

```bash
cp example/.env.example .env
```

Available options:
- `CONNECTLIFE_TOKEN_FILE` - Custom token storage location
- `LOG_LEVEL` - DEBUG/INFO/WARNING/ERROR

## Files

- `connectlife_cli.py` - Main CLI script
- `standalone_connectlife/` - Core library
- `example/` - Examples and documentation
- `requirements.txt` - Python dependencies

## License

MIT License
