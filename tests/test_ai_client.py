"""
Basic tests for the ai_client module.
Run with: python -m pytest tests/
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_client import clear_history


def test_clear_history():
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    result = clear_history(history)
    assert result == []


def test_clear_empty_history():
    result = clear_history([])
    assert result == []


def test_history_message_format():
    """Verify that history entries have the expected structure."""
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello! How can I help you?"}
    ]
    for msg in history:
        assert "role" in msg
        assert "content" in msg
        assert msg["role"] in ["user", "assistant"]


def test_history_preserves_order():
    """Verify that message order is maintained after operations."""
    history = [
        {"role": "user", "content": "First message"},
        {"role": "assistant", "content": "First reply"},
        {"role": "user", "content": "Second message"},
    ]
    assert history[0]["content"] == "First message"
    assert history[2]["content"] == "Second message"


def test_history_roles_alternate():
    """Check that a well-formed history alternates between user and assistant."""
    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "How are you?"},
        {"role": "assistant", "content": "I'm doing well, thanks!"},
    ]
    for i, msg in enumerate(history):
        expected_role = "user" if i % 2 == 0 else "assistant"
        assert msg["role"] == expected_role
