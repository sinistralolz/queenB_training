
from queenbee.domain.model import Alert


class MemoryNotifier:
    """Conserve les alertes en mémoire pour les tests."""

    def __init__(self) -> None:
        self.received: list[Alert] = []

    def send(self, alert: Alert) -> None:
        self.received.append(alert)
