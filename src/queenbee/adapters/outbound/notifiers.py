
"""Système de notification des alertes de Queen Bee."""

from collections.abc import Iterable

from queenbee.domain.model import Alert
from queenbee.domain.ports import AlertNotifier


class MemoryNotifier:
    """Conserve les alertes en mémoire pour les tests."""

    def __init__(self) -> None:
        self.received: list[Alert] = []

    def send(self, alert: Alert) -> None:
        self.received.append(alert)


class ObserverNotifier:
    """Diffuse les alertes à plusieurs abonnés."""

    def __init__(
        self,
        subscribers: Iterable[AlertNotifier] = (),
    ) -> None:
        self.subscribers = list(subscribers)
        self.failed_notifications = 0

    def subscribe(self, notifier: AlertNotifier) -> None:
        """Ajoute un destinataire."""
        self.subscribers.append(notifier)

    def unsubscribe(self, notifier: AlertNotifier) -> None:
        """Retire un destinataire."""
        self.subscribers.remove(notifier)

    def send(self, alert: Alert) -> None:
        """Envoie une alerte à tous les destinataires."""

        for subscriber in self.subscribers:
            try:
                subscriber.send(alert)
            except Exception:
                # Une panne ne doit pas bloquer les autres abonnés.
                self.failed_notifications += 1
