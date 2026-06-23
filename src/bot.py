import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from ai_client import get_ai_response, clear_history, get_history_summary

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Almacena el historial de conversación por usuario
conversation_history: dict[int, list] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensaje de bienvenida."""
    user = update.effective_user
    await update.message.reply_text(
        f"¡Hola {user.first_name}! 👋 Soy un bot con IA.\n\n"
        "Podés escribirme cualquier cosa y te respondo.\n\n"
        "Comandos disponibles:\n"
        "/start — mostrar este mensaje\n"
        "/clear — limpiar el historial de conversación\n"
        "/history — ver resumen de la conversación\n"
        "/help — ayuda"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra ayuda."""
    await update.message.reply_text(
        "💡 *Cómo usarme:*\n\n"
        "Simplemente escribime cualquier mensaje y te respondo con IA.\n\n"
        "Recuerdo el contexto de nuestra conversación, así que podés hacer preguntas de seguimiento.\n\n"
        "*Comandos:*\n"
        "/clear — borrar historial (empezar conversación nueva)\n"
        "/history — ver resumen de lo que hablamos",
        parse_mode="Markdown"
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Limpia el historial del usuario."""
    user_id = update.effective_user.id
    if user_id in conversation_history:
        conversation_history[user_id] = []
    await update.message.reply_text("🗑️ Historial borrado. ¡Empezamos de cero!")


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra un resumen de la conversación."""
    user_id = update.effective_user.id
    history = conversation_history.get(user_id, [])

    if not history:
        await update.message.reply_text("No hay conversación aún. ¡Escribime algo!")
        return

    await update.message.reply_text("⏳ Generando resumen...")
    summary = get_history_summary(history)
    await update.message.reply_text(f"📋 *Resumen de la conversación:*\n\n{summary}", parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes de texto del usuario."""
    user_id = update.effective_user.id
    user_message = update.message.text

    # Inicializa historial si no existe
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Indicador de escritura
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Obtiene respuesta de la IA
    response, updated_history = get_ai_response(
        message=user_message,
        history=conversation_history[user_id]
    )

    # Actualiza historial
    conversation_history[user_id] = updated_history

    await update.message.reply_text(response)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Maneja errores globales."""
    logger.error("Error al procesar update:", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "❌ Ocurrió un error. Por favor intentá de nuevo."
        )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("No se encontró TELEGRAM_BOT_TOKEN en el archivo .env")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("Bot iniciado. Presioná Ctrl+C para detener.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
