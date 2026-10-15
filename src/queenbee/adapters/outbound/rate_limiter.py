
"""Limitation du nombre d'alertes transmises."""

from collections.abc import Callable
from time import monotonic

from queenbee.domain.model import Alert
from queenbee.domain.ports import AlertNotifier


class RateLimitedNotifier:
    """Limite le nombre d'alertes transmises."""

    def __init__(
        self,
        notifier: AlertNotifier,
        max_per_window: int = 3,
        window_s: float = 60.0,
        clock: Callable[[], float] | None = None,
    ) -> None:
        if max_per_window <= 0 or window_s <= 0:
            raise ValueError("Limites invalides")

        if clock is None:
            clock = monotonic

        self.notifier = notifier
        self.max_per_window = max_per_window
        self.window_s = window_s
        self.clock = clock

        self.sent = 0
        self.dropped = 0
        self.window_start = self.clock()
        self.window_count = 0

    def send(self, alert: Alert) -> None:
        """Transmet l'alerte uniquement si la limite le permet."""

        now = self.clock()

        if now - self.window_start >= self.window_s:
            self.window_start = now
            self.window_count = 0

        if self.window_count >= self.max_per_window:
            self.dropped += 1
            return

        self.notifier.send(alert)
        self.window_count += 1
        self.sent += 1
