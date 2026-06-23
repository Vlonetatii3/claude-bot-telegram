# Telegram AI Bot

A Telegram bot powered by the Claude API (Anthropic). It maintains per-user conversation context, supports natural multi-turn dialogue, and includes utility commands for translation and summarization.

## Features

- Natural conversation with persistent context per user
- Responds in the same language the user writes in
- AI-generated conversation summaries
- Text translation to any language
- Text summarization
- Per-user message statistics
- Typing indicator while the bot processes a response

## Project structure

```
claude-bot-telegram/
├── src/
│   ├── bot.py          # Telegram bot logic and command handlers
│   └── ai_client.py    # Claude API client and AI utility functions
├── tests/
│   └── test_ai_client.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Vlonetatii3/claude-bot-telegram.git
cd claude-bot-telegram
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your credentials

**Telegram bot token:**
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Copy the token you receive

**Anthropic API key:**
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an account and generate an API key

### 5. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 6. Run the bot

```bash
python src/bot.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Show the welcome message and command list |
| `/help` | Show usage instructions |
| `/clear` | Erase the conversation history and start fresh |
| `/history` | Get an AI-generated summary of the conversation |
| `/stats` | Show your message count and session statistics |
| `/translate <language> <text>` | Translate text to any language |
| `/summarize <text>` | Get a concise summary of a block of text |
| `/about` | Show version and bot information |

### Examples

```
/translate French Good morning, how are you?
/summarize Paste a long article or paragraph here and get a concise summary.
```

## Running tests

```bash
python -m pytest tests/
```

## Customization

To change the bot's personality or behavior, edit `SYSTEM_PROMPT` in `src/ai_client.py`:

```python
SYSTEM_PROMPT = """You are an expert Python tutor helping developers learn..."""
```

To adjust the maximum number of messages kept in context, change `MAX_HISTORY_MESSAGES` in the same file (default: 20).

## Technologies

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) - Claude API client
- [python-dotenv](https://github.com/theskumar/python-dotenv) - environment variable management

## License

MIT
