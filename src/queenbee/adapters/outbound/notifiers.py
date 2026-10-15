
"""Système de notification des alertes de Queen Bee."""

import logging
from collections.abc import Iterable
from typing import Protocol

from queenbee.adapters.outbound.rate_limiter import RateLimitedNotifier
from queenbee.domain.model import Alert
from queenbee.domain.ports import AlertNotifier

__all__ = ["RateLimitedNotifier"]

audit_logger = logging.getLogger("queenbee.audit")


class NotificationTarget(Protocol):
    """Destinataire acceptant la méthode notify."""

    def notify(self, alert: Alert) -> None: ...


class MemoryNotifier:
    """Conserve les alertes en mémoire pour les tests."""

    def __init__(self) -> None:
        self.received: list[Alert] = []

    def send(self, alert: Alert) -> None:
        self.received.append(alert)

    def notify(self, alert: Alert) -> None:
        self.send(alert)


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

    def notify(self, alert: Alert) -> None:
        self.send(alert)


class AuditedNotifier:
    """Ajoute une trace d'audit avant chaque notification."""

    def __init__(self, notifier: NotificationTarget) -> None:
        self.notifier = notifier

    def notify(self, alert: Alert) -> None:
        audit_logger.info(
            "Notification de sécurité : règle=%s, source=%s",
            alert.rule,
            alert.source_ip,
        )
        self.notifier.notify(alert)

    def send(self, alert: Alert) -> None:
        self.notify(alert)
