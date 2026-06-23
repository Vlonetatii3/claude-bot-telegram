import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a friendly and helpful assistant on Telegram.
You respond in the same language the user writes in.
Your answers are concise and clear, suited for a messaging chat.
Avoid overly long responses unless the user explicitly asks for detail.
If you do not know something, say so honestly."""

MAX_HISTORY_MESSAGES = 20


def get_ai_response(message: str, history: list) -> tuple[str, list]:
    """
    Send a message to Claude and return the response plus the updated history.

    Args:
        message: The user's message.
        history: List of previous messages [{"role": "user/assistant", "content": "..."}]

    Returns:
        Tuple of (response_text, updated_history)
    """
    updated_history = history + [{"role": "user", "content": message}]

    if len(updated_history) > MAX_HISTORY_MESSAGES:
        updated_history = updated_history[-MAX_HISTORY_MESSAGES:]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=updated_history
    )

    assistant_message = response.content[0].text

    updated_history = updated_history + [{"role": "assistant", "content": assistant_message}]

    return assistant_message, updated_history


def get_history_summary(history: list) -> str:
    """
    Generate a summary of the conversation using AI.

    Args:
        history: List of conversation messages.

    Returns:
        Summary as plain text.
    """
    if not history:
        return "No conversation to summarize."

    conversation_text = "\n".join(
        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
        for msg in history
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"Summarize this conversation in 3-5 key points:\n\n{conversation_text}"
        }]
    )

    return response.content[0].text


def translate_text(text: str, target_language: str) -> str:
    """
    Translate the given text into the target language using AI.

    Args:
        text: The text to translate.
        target_language: The language to translate into (e.g. "Spanish", "French").

    Returns:
        Translated text.
    """
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"Translate the following text to {target_language}. "
                "Return only the translation, no explanations or extra text.\n\n"
                f"{text}"
            )
        }]
    )

    return response.content[0].text


def summarize_text(text: str) -> str:
    """
    Summarize the given text using AI.

    Args:
        text: The text to summarize.

    Returns:
        A concise summary.
    """
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                "Please provide a clear and concise summary of the following text. "
                "Capture the main points and key information:\n\n"
                f"{text}"
            )
        }]
    )

    return response.content[0].text


def clear_history(history: list) -> list:
    """Clear the conversation history."""
    return []
