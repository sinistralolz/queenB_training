
from typing import Protocol

from queenbee.domain.model import Alert, Incident


class IncidentRepository(Protocol):
    """Contrat pour enregistrer un incident."""

    def save(self, incident: Incident) -> None:
        ...


class IncidentReader(Protocol):
    """Contrat pour consulter les incidents."""

    def list_all(self) -> list[Incident]:
        ...


class AlertNotifier(Protocol):
    """Contrat pour envoyer une alerte."""

    def send(self, alert: Alert) -> None:
        ...
