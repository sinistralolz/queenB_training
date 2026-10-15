
"""Adaptateur entrant pour les journaux SSH."""

import re
from datetime import datetime

from queenbee.domain.model import DomainError, SecurityEvent

SSH_FAILURE_PATTERN = re.compile(
    r"(?P<timestamp>\S+) sshd: Failed password for "
    r"(?P<username>[a-zA-Z0-9_.-]{1,64}) "
    r"from (?P<source_ip>[0-9a-fA-F:.]+)"
)


def parse_sshd_line(line: str) -> SecurityEvent:
    """Transforme une ligne SSH valide en événement de sécurité."""

    if not isinstance(line, str):
        raise DomainError("Le journal doit être une chaîne de caractères")

    if not line or len(line) > 4096 or "\x00" in line:
        raise DomainError("Journal SSH invalide ou trop long")

    match = SSH_FAILURE_PATTERN.fullmatch(line)

    if match is None:
        raise DomainError("Format du journal SSH non reconnu")

    try:
        timestamp = datetime.fromisoformat(match.group("timestamp"))
    except ValueError as exc:
        raise DomainError("Date du journal SSH invalide") from exc

    return SecurityEvent(
        source_ip=match.group("source_ip"),
        username=match.group("username"),
        action="login_failed",
        timestamp=timestamp,
    )
