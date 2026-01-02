# Plan: Telegram Bot for tmux Control & Notifications

## Overview
Create a Telegram bot that:
1. Receives notifications from Claude Code (alternative to notify-send)
2. Controls tmux sessions remotely (send commands, read output, switch windows)

## Feasibility: ✅ Highly Feasible
- Complexity: Medium (3-5 days MVP, 1-2 weeks production)
- All required components exist and are well-documented

## Tech Stack

```
python-telegram-bot  # Bot API (mature, well-documented)
libtmux              # tmux control (typed, object-oriented)
python-dotenv        # config management
systemd              # deployment (auto-restart, logging)
```

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Telegram   │────▶│  Bot (py)   │────▶│   tmux      │
│  (phone)    │◀────│  + libtmux  │◀────│  sessions   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │  Skillbox   │
                    │  Hooks      │
                    └─────────────┘
```

## Bot Commands (MVP)

```
/list              - list all tmux sessions
/send <sess> <cmd> - send command to session
/capture <sess>    - capture pane output
/windows <sess>    - list windows in session
/panes <sess:win>  - list panes
/create <sess>     - create new session
/kill <sess>       - kill session
```

## Security Model

1. **User Whitelist** — Telegram user IDs (get via @userinfobot)
2. **Token Protection** — environment variables, never in code
3. **Command Validation** — whitelist allowed commands
4. **Rate Limiting** — built-in to python-telegram-bot
5. **Audit Logging** — log all commands with user ID

### Authentication Decorator
```python
ALLOWED_USERS = [123456789]  # Telegram user IDs

def authorized_only(func):
    async def wrapper(update, context):
        if update.effective_user.id not in ALLOWED_USERS:
            await update.message.reply_text("⛔ Unauthorized")
            return
        return await func(update, context)
    return wrapper
```

## Key Code Examples

### List Sessions
```python
import libtmux

server = libtmux.Server()
sessions = [s.name for s in server.sessions]
```

### Send Command
```python
session = server.sessions.get(session_name="main")
pane = session.active_window.active_pane
pane.send_keys("echo hello", enter=True)
```

### Capture Output
```python
output = pane.cmd('capture-pane', '-p').stdout
```

### Send Notification
```python
import requests

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})
```

## Deployment (systemd)

```ini
# /etc/systemd/system/telegram-tmux-bot.service
[Unit]
Description=Telegram tmux Control Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/telegram-bot
Environment=TELEGRAM_BOT_TOKEN=xxx
ExecStart=/usr/bin/python3 bot.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Integration with Skillbox

### Option 1: Alternative Notifier
Add to `lib/notifier.py`:
```python
def notify_telegram(title: str, message: str) -> bool:
    """Send notification to Telegram."""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        return False
    # ... send via API
```

### Option 2: Separate Hook
Create `telegram-notify.py` hook that sends to Telegram on Stop/Notification events.

## Implementation Phases

### Phase 1: MVP (Week 1)
- [ ] Basic bot with polling
- [ ] User whitelist authentication
- [ ] Commands: /list, /send, /capture
- [ ] Local testing

### Phase 2: Production (Week 2)
- [ ] systemd service
- [ ] Error handling
- [ ] Audit logging
- [ ] Webhooks (optional)

### Phase 3: Skillbox Integration (Week 3)
- [ ] Notification helper script
- [ ] Hook integration
- [ ] Interactive session browser
- [ ] Documentation

## Resources

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [libtmux](https://github.com/tmux-python/libtmux)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Related Projects

- Terminal_bot (RodrigoDePool) — basic terminal via Telegram
- ShellRemoteBot (Al-Muhandis) — full SSH emulator via Telegram
