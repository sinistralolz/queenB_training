

"""Adaptateur sécurisé pour les journaux SSH."""

import re
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from queenbee.domain.model import DomainError, SecurityEvent


MAX_LINE_LENGTH = 4096

SSH_FAILURE = re.compile(
    r"Failed password for (?P<user>[A-Za-z0-9_.-]{1,64}) "
    r"from (?P<ip>(?:[0-9]{1,3}\.){3}[0-9]{1,3})"
)


def parse_ssh_failure(
    line: str,
    timestamp: datetime,
) -> SecurityEvent | None:
    """Transforme une ligne SSH valide en événement de sécurité."""

    # Refuser les entrées trop longues.
    if len(line) > MAX_LINE_LENGTH:
        return None

    # Refuser les caractères nuls.
    if "\x00" in line:
        return None

    # Retirer uniquement la fin de ligne.
    clean_line = line.removesuffix("\n").removesuffix("\r")

    # La ligne entière doit correspondre au format attendu.
    match = SSH_FAILURE.fullmatch(clean_line)

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
    path: str | Path,
    timestamp: datetime,
) -> Iterator[SecurityEvent]:
    """Lit un fichier de logs sans accepter les lignes malveillantes."""

    with open(path, encoding="utf-8", errors="replace") as logfile:
        while True:
            line = logfile.readline(MAX_LINE_LENGTH + 2)

            if not line:
                break

            if len(line) > MAX_LINE_LENGTH:
                # Ignorer le reste de la ligne trop longue.
                if not line.endswith("\n"):
                    for fragment in logfile:
                        if fragment.endswith("\n"):
                            break
                continue

            event = parse_ssh_failure(line, timestamp)

            if event is not None:
                yield event
