import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Eres un asistente amigable y útil en Telegram. 
Respondés en el mismo idioma que el usuario.
Tus respuestas son concisas y claras, apropiadas para un chat de mensajería.
Evitás respuestas demasiado largas a menos que el usuario lo pida explícitamente.
Si no sabés algo, lo decís honestamente."""

MAX_HISTORY_MESSAGES = 20  # Máximo de mensajes en el historial


def get_ai_response(message: str, history: list) -> tuple[str, list]:
    """
    Envía un mensaje a Claude y retorna la respuesta + historial actualizado.
    
    Args:
        message: El mensaje del usuario.
        history: Lista de mensajes previos [{"role": "user/assistant", "content": "..."}]
    
    Returns:
        Tupla de (respuesta_texto, historial_actualizado)
    """
    # Agrega el nuevo mensaje al historial
    updated_history = history + [{"role": "user", "content": message}]

    # Limita el historial para no exceder el contexto
    if len(updated_history) > MAX_HISTORY_MESSAGES:
        updated_history = updated_history[-MAX_HISTORY_MESSAGES:]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=updated_history
    )

    assistant_message = response.content[0].text

    # Agrega la respuesta del asistente al historial
    updated_history = updated_history + [{"role": "assistant", "content": assistant_message}]

    return assistant_message, updated_history


def get_history_summary(history: list) -> str:
    """
    Genera un resumen de la conversación usando IA.
    
    Args:
        history: Lista de mensajes de la conversación.
    
    Returns:
        Resumen en texto.
    """
    if not history:
        return "No hay conversación para resumir."

    conversation_text = "\n".join(
        f"{'Usuario' if msg['role'] == 'user' else 'Asistente'}: {msg['content']}"
        for msg in history
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"Resumí esta conversación en 3-5 puntos clave:\n\n{conversation_text}"
        }]
    )

    return response.content[0].text


def clear_history(history: list) -> list:
    """Limpia el historial de conversación."""
    return []
