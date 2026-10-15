
"""Ports utilisés par les services applicatifs de Queen Bee."""

from typing import Protocol

from queenbee.domain.model import Alert, Incident


class IncidentRepository(Protocol):
    """Contrat pour enregistrer et retrouver des incidents."""

    def save(self, incident: Incident) -> None:
        """Enregistre un incident."""
        ...

    def get_by_id(self, incident_id: str) -> Incident | None:
        """Recherche un incident par son identifiant."""
        ...


class Notifier(Protocol):
    """Contrat pour transmettre une alerte."""

    def send(self, alert: Alert) -> None:
        """Envoie une alerte."""
        ...


class Firewall(Protocol):
    """Contrat pour appliquer des actions de blocage réseau."""

    def block_ip(self, ip: str) -> None:
        """Bloque une adresse IP."""
        ...

    def unblock_ip(self, ip: str) -> None:
        """Annule le blocage d'une adresse IP."""
        ...
