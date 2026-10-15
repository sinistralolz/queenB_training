
"""Contrôle d'accès à la consultation des incidents."""

from queenbee.application.services import AccessDeniedError
from queenbee.domain.model import Incident, Principal


class IncidentReadProxy:
    """Autorise la consultation des incidents selon les rôles."""

    def __init__(self, repository: object, principal: Principal) -> None:
        self.repository = repository
        self.principal = principal

    def list_open(self) -> list[Incident]:
        """Retourne les incidents ouverts aux utilisateurs autorisés."""

        if not self.principal.roles.intersection({"viewer", "analyst", "admin"}):
            raise AccessDeniedError("Accès refusé : rôle insuffisant")

        if not hasattr(self.repository, "list_open"):
            raise TypeError("Le dépôt ne permet pas de consulter les incidents")

        result: list[Incident] = self.repository.list_open()
        return result
