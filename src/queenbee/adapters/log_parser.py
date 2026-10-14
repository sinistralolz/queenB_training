
"""Analyse sécurisée des journaux SSH."""

import re
from collections.abc import Iterator
from pathlib import Path

from queenbee.domain.model import DomainError, SecurityEvent

from datetime import datetime

SSH_FAILURE = re.compile(
    r"^Failed password for (?P<user>[A-Za-z0-9_.-]{1,64}) "
    r"from (?P<ip>(?:[0-9]{1,3}\.){3}[0-9]{1,3})$"
)

MAX_LINE_LENGTH = 4096


def parse_ssh_failure(line: str, timestamp: datetime) -> SecurityEvent | None:
    """Transforme une ligne SSH valide en événement de sécurité."""

    if len(line) > MAX_LINE_LENGTH:
        return None

    match = SSH_FAILURE.fullmatch(line.strip())

    if match is None:
        return None

    try:
        return SecurityEvent(
            source_ip=match.group("ip"),
            username=match.group("user"),
            action="login_failed",
            timestamp=timestamp,
        )
    except DomainError:
        return None


def read_ssh_failures(
    path: str | Path, timestamp: datetime
) -> Iterator[SecurityEvent]:
    """Lit un fichier de logs en limitant la taille des lignes."""

    with open(path, encoding="utf-8", errors="replace") as logfile:
        while True:
            line = logfile.readline(MAX_LINE_LENGTH + 2)

            if not line:
                break

            if len(line) > MAX_LINE_LENGTH:
                if not line.endswith("\n"):
                    for fragment in logfile:
                        if fragment.endswith("\n"):
                            break
                continue

            event = parse_ssh_failure(line, timestamp)

            if event is not None:
                yield event
