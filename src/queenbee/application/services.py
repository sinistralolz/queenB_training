
"""Services applicatifs de Queen Bee."""

from collections.abc import Iterable
from typing import cast
from uuid import UUID

from queenbee.domain.model import (
    DomainError,
    Incident,
    IncidentStatus,
    Principal,
    SecurityEvent,
)
from queenbee.domain.ports import AlertNotifier, IncidentRepository
from queenbee.domain.rules import DetectionRule


class AccessDeniedError(PermissionError):
    """L'utilisateur n'a pas les autorisations nécessaires."""


class DetectionService:
    """Détecte les alertes et crée les incidents correspondants."""

    def __init__(
        self,
        rule: DetectionRule,
        repository: IncidentRepository,
        notifiers: Iterable[AlertNotifier],
    ) -> None:
        self.rule = rule
        self.repository = repository
        self.notifiers = tuple(notifiers)

    def ingest(self, events: Iterable[SecurityEvent]) -> list[Incident]:
        """Analyse les événements, enregistre et retourne les incidents."""

        alerts = self.rule.evaluate(events)
        created: list[Incident] = []

        for alert in alerts:
            incident = Incident(alert)
            self.repository.save(incident)
            created.append(incident)

            for notifier in self.notifiers:
                if hasattr(notifier, "notify"):
                    notifier.notify(alert)
                else:
                    notifier.send(alert)

        return created


class IncidentService:
    """Gère les changements d'état des incidents."""

    def __init__(self, repository: IncidentRepository) -> None:
        self.repository = repository

    def move(
        self,
        who: Principal,
        incident_id: UUID,
        to: IncidentStatus,
    ) -> Incident:
        """Vérifie les droits puis change l'état d'un incident."""

        # 1. Vérifier les autorisations avant toute consultation.
        if "analyst" not in who.roles and "admin" not in who.roles:
            raise AccessDeniedError("Accès refusé : rôle analyste requis")

        # 2. Retrouver l'incident.
        repository = cast("IncidentLookup", self.repository)
        incident = repository.get(incident_id)

        # 3. Appliquer les règles métier.
        incident.transition_to(to)

        # 4. Enregistrer le nouvel état.
        self.repository.save(incident)

        return incident


class IncidentLookup:
    """Interface minimale pour rechercher un incident."""

    def get(self, incident_id: UUID) -> Incident:
        raise NotImplementedError

