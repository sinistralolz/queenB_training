
"""Tests complémentaires de sécurité de l'API des agents."""

import json
from datetime import UTC, datetime

import pytest

from queenbee.adapters.inbound.agent_api import (
    UnauthenticatedError,
    parse_agent_message,
    sign,
)
from queenbee.domain.model import DomainError


KEY = b"queenbee-test-secret-key"
TIMESTAMP = datetime(2026, 10, 15, tzinfo=UTC).isoformat()


def make_body(**changes: object) -> bytes:
    """Construit un message d'agent pour les tests."""
    data: dict[str, object] = {
        "source_ip": "10.0.0.66",
        "username": "alice",
        "action": "login_failed",
        "timestamp": TIMESTAMP,
    }
    data.update(changes)
    return json.dumps(data).encode("utf-8")


def parse_signed(body: bytes):
    """Signe un message avant de le faire analyser."""
    return parse_agent_message(body, sign(body, KEY), KEY)


def test_rejects_oversized_message() -> None:
    """Un message dépassant 4096 octets est refusé."""
    body = b"X" * 4097

    with pytest.raises(DomainError, match="trop volumineux"):
        parse_signed(body)


def test_rejects_non_bytes_message() -> None:
    """Un message qui n'est pas en bytes est refusé."""
    with pytest.raises(DomainError, match="Message invalide"):
        parse_agent_message("texte", "signature", KEY)  # type: ignore[arg-type]


def test_rejects_non_string_signature() -> None:
    """Une signature qui n'est pas une chaîne est refusée."""
    body = make_body()

    with pytest.raises(UnauthenticatedError, match="Signature invalide"):
        parse_agent_message(body, 123, KEY)  # type: ignore[arg-type]


def test_rejects_invalid_json() -> None:
    """Un JSON malformé est rejeté même avec une signature correcte."""
    body = b"{invalid-json"

    with pytest.raises(DomainError, match="JSON invalide"):
        parse_signed(body)


def test_rejects_json_array() -> None:
    """Un tableau JSON n'est pas un message d'agent valide."""
    body = b"[]"

    with pytest.raises(DomainError, match="Structure du message"):
        parse_signed(body)


def test_rejects_invalid_field_type() -> None:
    """Les champs doivent tous contenir des chaînes."""
    body = make_body(username=123)

    with pytest.raises(DomainError, match="Types de données"):
        parse_signed(body)


def test_rejects_invalid_timestamp() -> None:
    """Une date incorrecte est rejetée."""
    body = make_body(timestamp="pas-une-date")

    with pytest.raises(DomainError, match="Date invalide"):
        parse_signed(body)


def test_accepts_valid_signed_message() -> None:
    """Un message correctement signé et valide est accepté."""
    body = make_body()

    event = parse_signed(body)

    assert event.source_ip == "10.0.0.66"
    assert event.username == "alice"
    assert event.action == "login_failed"
