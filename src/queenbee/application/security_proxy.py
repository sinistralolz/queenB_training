
from collections.abc import Iterable

from queenbee.domain.model import Incident
from queenbee.domain.ports import IncidentReader


class AccessDeniedError(Exception):
    """Accès refusé à un utilisateur non autorisé."""


class IncidentReaderProxy:
    """Contrôle les droits avant de consulter les incidents."""

    def __init__(
        self,
        reader: IncidentReader,
        roles: Iterable[str],
    ) -> None:
        self.reader = reader
        self.roles = frozenset(roles)

    def list_all(self) -> list[Incident]:
        """Autorise uniquement les viewers et analystes."""

        if not self.roles.intersection({"viewer", "analyst"}):
            raise AccessDeniedError("Accès aux incidents refusé")

        return self.reader.list_all()
