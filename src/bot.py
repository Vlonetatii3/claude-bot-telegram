import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from ai_client import get_ai_response, clear_history, get_history_summary, translate_text, summarize_text

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_VERSION = "1.1.0"

# Stores per-user conversation history and message counts
conversation_history: dict[int, list] = {}
message_counts: dict[int, int] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message shown on /start."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! I am an AI-powered Telegram bot.\n\n"
        "You can write me anything and I will respond.\n\n"
        "Available commands:\n"
        "/start - show this message\n"
        "/help - show help\n"
        "/clear - clear the conversation history\n"
        "/history - view a summary of the conversation\n"
        "/stats - show your conversation statistics\n"
        "/translate <language> <text> - translate text to a language\n"
        "/summarize <text> - summarize a block of text\n"
        "/about - about this bot"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show usage help."""
    await update.message.reply_text(
        "*How to use me:*\n\n"
        "Just send me any message and I will reply using AI.\n\n"
        "I remember the context of our conversation, so you can ask follow-up questions.\n\n"
        "*Commands:*\n"
        "/clear - erase history and start a new conversation\n"
        "/history - get a summary of what we discussed\n"
        "/stats - see how many messages you have sent\n"
        "/translate <language> <text> - translate text to any language\n"
        "  Example: `/translate French Hello, how are you?`\n"
        "/summarize <text> - get a concise summary of a long text\n"
        "/about - version and info",
        parse_mode="Markdown"
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear the user's conversation history."""
    user_id = update.effective_user.id
    if user_id in conversation_history:
        conversation_history[user_id] = []
    await update.message.reply_text("History cleared. Starting fresh!")


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show an AI-generated summary of the conversation."""
    user_id = update.effective_user.id
    history = conversation_history.get(user_id, [])

    if not history:
        await update.message.reply_text("No conversation yet. Send me a message!")
        return

    await update.message.reply_text("Generating summary...")
    summary = get_history_summary(history)
    await update.message.reply_text(
        f"*Conversation summary:*\n\n{summary}",
        parse_mode="Markdown"
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the user's conversation statistics."""
    user_id = update.effective_user.id
    history = conversation_history.get(user_id, [])
    total_messages = message_counts.get(user_id, 0)

    user_turns = sum(1 for msg in history if msg["role"] == "user")
    assistant_turns = sum(1 for msg in history if msg["role"] == "assistant")

    await update.message.reply_text(
        "*Your conversation stats:*\n\n"
        f"Total messages sent (all time): {total_messages}\n"
        f"Messages in current session: {user_turns}\n"
        f"Bot replies in current session: {assistant_turns}",
        parse_mode="Markdown"
    )


async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Translate text to a specified language. Usage: /translate <language> <text>"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: `/translate <language> <text>`\n"
            "Example: `/translate Spanish Good morning, how are you?`",
            parse_mode="Markdown"
        )
        return

    target_language = context.args[0]
    text_to_translate = " ".join(context.args[1:])

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    translated = translate_text(text_to_translate, target_language)

    await update.message.reply_text(
        f"*Translation to {target_language}:*\n\n{translated}",
        parse_mode="Markdown"
    )


async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Summarize a block of text. Usage: /summarize <text>"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/summarize <text>`\n"
            "Example: `/summarize Paste a long article or paragraph here...`",
            parse_mode="Markdown"
        )
        return

    text_to_summarize = " ".join(context.args)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    summary = summarize_text(text_to_summarize)

    await update.message.reply_text(
        f"*Summary:*\n\n{summary}",
        parse_mode="Markdown"
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show information about the bot."""
    await update.message.reply_text(
        f"*Telegram AI Bot v{BOT_VERSION}*\n\n"
        "An AI-powered Telegram bot built with the Claude API (Anthropic) "
        "and python-telegram-bot.\n\n"
        "It maintains per-user conversation context and supports translation, "
        "summarization, and natural conversation.\n\n"
        "Source: github.com/Vlonetatii3/claude-bot-telegram",
        parse_mode="Markdown"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages."""
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Track total message count across all sessions
    message_counts[user_id] = message_counts.get(user_id, 0) + 1

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    response, updated_history = get_ai_response(
        message=user_message,
        history=conversation_history[user_id]
    )

    conversation_history[user_id] = updated_history

    await update.message.reply_text(response)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle uncaught errors globally."""
    logger.error("Error while processing update:", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "An error occurred. Please try again."
        )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("translate", translate_command))
    app.add_handler(CommandHandler("summarize", summarize_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
