
from typing import cast

from queenbee.adapters.outbound.notifiers import (
    MemoryNotifier,
    ObserverNotifier,
)
from queenbee.domain.model import Alert


class BrokenNotifier:
    """Simule un destinataire en panne."""

    def __init__(self) -> None:
        self.attempts = 0

    def send(self, alert: Alert) -> None:
        self.attempts += 1
        raise RuntimeError("Service de notification indisponible")


def test_observer_notifies_all_subscribers() -> None:
    """Tous les abonnés reçoivent la même alerte."""

    first = MemoryNotifier()
    second = MemoryNotifier()

    observer = ObserverNotifier([first, second])
    alert = cast(Alert, object())

    observer.send(alert)

    assert first.received == [alert]
    assert second.received == [alert]
    assert observer.failed_notifications == 0


def test_abuse_broken_subscriber_does_not_block_others() -> None:
    """Un destinataire en panne ne bloque pas les autres."""

    first = MemoryNotifier()
    broken = BrokenNotifier()
    second = MemoryNotifier()

    observer = ObserverNotifier([first, broken, second])
    alert = cast(Alert, object())

    observer.send(alert)

    assert first.received == [alert]
    assert broken.attempts == 1
    assert second.received == [alert]
    assert observer.failed_notifications == 1


def test_observer_can_unsubscribe() -> None:
    """Un abonné retiré ne reçoit plus d'alertes."""

    first = MemoryNotifier()
    second = MemoryNotifier()

    observer = ObserverNotifier([first, second])
    observer.unsubscribe(second)

    alert = cast(Alert, object())
    observer.send(alert)

    assert first.received == [alert]
    assert second.received == []
