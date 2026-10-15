
"""Réception sécurisée des messages des agents Queen Bee."""

import hashlib
import hmac
import json
from datetime import datetime

from queenbee.domain.model import DomainError, SecurityEvent

MAX_MESSAGE_SIZE = 4096

REQUIRED_FIELDS = {
    "source_ip",
    "username",
    "action",
    "timestamp",
}


class UnauthenticatedError(PermissionError):
    """Le message ne possède pas une signature HMAC valide."""


def sign(body: bytes, key: bytes) -> str:
    """Calcule la signature HMAC-SHA256 d'un message."""

    return hmac.new(key, body, hashlib.sha256).hexdigest()


def parse_agent_message(
    body: bytes,
    signature: str,
    key: bytes,
) -> SecurityEvent:
    """Authentifie et valide un message envoyé par un agent."""

    if not isinstance(body, bytes) or len(body) > MAX_MESSAGE_SIZE:
        raise DomainError("Message invalide ou trop volumineux")

    if not isinstance(signature, str):
        raise UnauthenticatedError("Signature invalide")

    expected_signature = sign(body, key)

    if not hmac.compare_digest(signature, expected_signature):
        raise UnauthenticatedError("Authentification refusée")

    try:
        data = json.loads(body)
    except (ValueError, UnicodeDecodeError) as exc:
        raise DomainError("JSON invalide") from exc

    if not isinstance(data, dict) or set(data) != REQUIRED_FIELDS:
        raise DomainError("Structure du message invalide")

    if not all(isinstance(value, str) for value in data.values()):
        raise DomainError("Types de données invalides")

    try:
        timestamp = datetime.fromisoformat(data["timestamp"])
    except ValueError as exc:
        raise DomainError("Date invalide") from exc

    return SecurityEvent(
        source_ip=data["source_ip"],
        username=data["username"],
        action=data["action"],
        timestamp=timestamp,
    )
