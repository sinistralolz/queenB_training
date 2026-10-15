
from collections.abc import Iterable

from queenbee.domain.model import Incident
from queenbee.domain.ports import IncidentReader


class AccessDeniedError(Exception):
    """Accès refusé à un utilisateur non autorisé."""


class IncidentReaderProxy:
    """Protège la consultation des incidents."""

    def __init__(self, reader: IncidentReader) -> None:
        self.reader = reader

    def list_all(self, roles: Iterable[str]) -> list[Incident]:
        """Vérifie les droits avant de consulter les incidents."""

        if not {"viewer", "analyst"}.intersection(roles):
            raise AccessDeniedError("Accès aux incidents refusé")

        return self.reader.list_all()
