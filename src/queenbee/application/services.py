
from collections.abc import Iterable

from queenbee.domain.model import Incident, SecurityEvent
from queenbee.domain.ports import AlertNotifier, IncidentRepository
from queenbee.domain.rules import DetectionRule


class DetectionService:
    def __init__(
        self,
        rule: DetectionRule,
        repository: IncidentRepository,
        notifiers: Iterable[AlertNotifier],
    ) -> None:
        self.rule = rule
        self.repository = repository
        self.notifiers = tuple(notifiers)

    def ingest(self, events: Iterable[SecurityEvent]) -> None:
        alerts = self.rule.evaluate(events)

        for alert in alerts:
            incident = Incident(alert)
            self.repository.save(incident)

            for notifier in self.notifiers:
                notifier.send(alert)
