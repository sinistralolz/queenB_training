
from typing import Protocol

from queenbee.adapters.outbound.notifiers import MemoryNotifier
from queenbee.adapters.outbound.repositories import (
    InMemoryIncidentRepository,
    SqliteIncidentRepository,
)
from queenbee.domain.ports import AlertNotifier, IncidentRepository


class ComponentFactory(Protocol):
    def repository(self) -> IncidentRepository:
        ...

    def notifier(self) -> AlertNotifier:
        ...


class InMemoryFactory:
    def repository(self) -> InMemoryIncidentRepository:
        return InMemoryIncidentRepository()

    def notifier(self) -> MemoryNotifier:
        return MemoryNotifier()


class ProdFactory:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def repository(self) -> SqliteIncidentRepository:
        return SqliteIncidentRepository(self.db_path)

    def notifier(self) -> AlertNotifier:
        raise NotImplementedError(
            "Le notificateur de production reste à configurer"
        )
