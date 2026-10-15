
"""Assemblage des composants de Queen Bee."""

from collections.abc import Iterable

from queenbee.adapters.inbound.log_parser import parse_sshd_line
from queenbee.adapters.outbound.repositories import InMemoryIncidentRepository
from queenbee.application.services import DetectionService
from queenbee.config import Settings
from queenbee.domain.model import DomainError, Incident, SecurityEvent
from queenbee.domain.ports import AlertNotifier
from queenbee.domain.rules import BruteForceRule
from queenbee.factories import InMemoryFactory, ProdFactory


def bootstrap(settings: Settings, production: bool = False) -> DetectionService:
    """Assemble les composants sans utiliser de Singleton."""

    factory = (
        ProdFactory(settings.database_path)
        if production
        else InMemoryFactory()
    )

    repository = factory.repository()

    if production:
        raise NotImplementedError(
            "Le notificateur de production reste à configurer"
        )

    notifier: AlertNotifier = factory.notifier()

    return DetectionService(
        rule=BruteForceRule(),
        repository=repository,
        notifiers=[notifier],
    )


class QueenBeeApp:
    """Façade pour recevoir et analyser les journaux SSH."""

    def __init__(self, service: DetectionService) -> None:
        self.service = service
        self.rejected = 0

    def ingest_lines(self, lines: Iterable[str]) -> list[Incident]:
        """Analyse les lignes valides et compte les lignes rejetées."""

        events: list[SecurityEvent] = []

        for line in lines:
            try:
                events.append(parse_sshd_line(line))
            except DomainError:
                self.rejected += 1

        return self.service.ingest(events)


def build_app(settings: Settings) -> QueenBeeApp:
    """Construit l'application avec ses composants en mémoire."""

    repository = InMemoryIncidentRepository()

    service = DetectionService(
        rule=BruteForceRule(),
        repository=repository,
        notifiers=[],
    )

    return QueenBeeApp(service)
