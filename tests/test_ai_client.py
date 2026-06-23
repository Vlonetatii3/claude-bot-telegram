"""
Tests básicos para el módulo ai_client.
Ejecutar con: python -m pytest tests/
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_client import clear_history, get_history_summary


def test_clear_history():
    history = [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "¡Hola!"}
    ]
    result = clear_history(history)
    assert result == []


def test_clear_empty_history():
    result = clear_history([])
    assert result == []


def test_history_format():
    """Verifica que el historial tenga el formato correcto."""
    history = [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "¡Hola! ¿Cómo puedo ayudarte?"}
    ]
    for msg in history:
        assert "role" in msg
        assert "content" in msg
        assert msg["role"] in ["user", "assistant"]
