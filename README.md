# WhatsApp Link Generator Telegram Bot

A Telegram bot that generates WhatsApp chat links with pre-filled messages.

## Features

- Generate WhatsApp chat links with custom messages
- Supports international phone numbers with country codes
- User-friendly step-by-step interaction
- Hindi language interface

## Deployment on Railway

1. Fork this repository
2. Create a new project on [Railway](https://railway.app/)
3. Connect your GitHub repository
4. Add environment variable:
   - `TOKEN`: Your Telegram bot token from BotFather

## Environment Variables

- `TOKEN`: Telegram Bot Token (Get it from [@BotFather](https://t.me/BotFather))

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variable:
   ```bash
   # Windows
   set TOKEN=your_bot_token_here
   
   # Linux/macOS
   export TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python whatsappAi.py
   ```

## Tech Stack

- Python 3.11+
- python-telegram-bot