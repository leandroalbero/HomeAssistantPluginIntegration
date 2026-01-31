# ConnectLife Standalone Client - Example Usage

## ⚠️ REQUIRED: Hosts File Configuration

Before using this tool, you MUST configure your hosts file to redirect `homeassistant.local` to your local machine:

### macOS/Linux

```bash
# Add to /etc/hosts
echo "127.0.0.1 homeassistant.local" | sudo tee -a /etc/hosts

# Flush DNS cache (macOS)
sudo killall -HUP mDNSResponder

# Flush DNS cache (Linux)
sudo systemd-resolve --flush-caches
```

### Windows

1. Open Notepad as Administrator
2. Open: `C:\Windows\System32\drivers\etc\hosts`
3. Add line: `127.0.0.1 homeassistant.local`
4. Save
5. Run in Command Prompt (as Admin): `ipconfig /flushdns`

### Why This Is Needed

The ConnectLife OAuth2 client is configured to redirect to `homeassistant.local:8123` (the same URL used by Home Assistant). This hosts file entry ensures the redirect comes back to your local machine.

## Setup

1. **Configure hosts file** (see above)

2. Copy the example .env file:

```bash
cp example/.env.example .env
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Authentication

### OAuth2 Browser Flow (Only Method Available)

```bash
python connectlife_cli.py --list-devices
```

Steps:
1. ✅ Script checks hosts file configuration
2. 🌐 A URL opens in your browser
3. 🔑 Log in with your ConnectLife account
4. 📋 Copy the callback URL (starts with `http://homeassistant.local:8123/...`)
5. 📋 Paste it back in the terminal

**Note:** After login, you'll see "Page not found" - this is expected! Just copy the URL from the address bar.

## Usage Examples

### List All Devices

```bash
python connectlife_cli.py --list-devices
```

### Show Device Status

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

## Troubleshooting

### "Hosts file not configured"

Run the hosts file setup commands in the section above.

### "Wrong email or password" on web

- Clear browser cookies
- Try incognito/private window
- Verify you can log into the ConnectLife mobile app

### "Page not found" after login

**This is expected!** The OAuth redirect goes to `homeassistant.local` which doesn't serve a real page. Copy the URL from your browser's address bar and paste it in the terminal.

## Files

- `.env.example` - Example configuration
- `README.md` - This file

See the main `STANDALONE_README.md` for complete documentation.
