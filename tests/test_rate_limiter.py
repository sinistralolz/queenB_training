
from typing import cast

import pytest

from queenbee.adapters.outbound.rate_limiter import RateLimitedNotifier
from queenbee.domain.model import Alert


class SpyNotifier:
    """Enregistre les alertes reçues pour les tests."""

    def __init__(self) -> None:
        self.received: list[Alert] = []

    def send(self, alert: Alert) -> None:
        self.received.append(alert)


def test_abuse_rate_limiter_absorbs_alert_flood() -> None:
    """1000 alertes : seulement 3 transmises."""

    spy = SpyNotifier()
    now = [0.0]

    limiter = RateLimitedNotifier(
        notifier=spy,
        max_per_window=3,
        window_s=60,
        clock=lambda: now[0],
    )

    alert = cast(Alert, object())

    for _ in range(1000):
        limiter.send(alert)

    assert len(spy.received) == 3
    assert limiter.sent == 3
    assert limiter.dropped == 997


def test_rate_limiter_resets_after_window() -> None:
    """Une nouvelle fenêtre permet de transmettre des alertes."""

    spy = SpyNotifier()
    now = [0.0]

    limiter = RateLimitedNotifier(
        notifier=spy,
        max_per_window=3,
        window_s=60,
        clock=lambda: now[0],
    )

    alert = cast(Alert, object())

    for _ in range(4):
        limiter.send(alert)

    assert len(spy.received) == 3
    assert limiter.dropped == 1

    now[0] = 61.0
    limiter.send(alert)

    assert len(spy.received) == 4


def test_abuse_invalid_rate_limit_is_rejected() -> None:
    """Une limite invalide doit être refusée."""

    with pytest.raises(ValueError):
        RateLimitedNotifier(
            notifier=SpyNotifier(),
            max_per_window=0,
        )
