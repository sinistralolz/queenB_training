
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from queenbee.domain.model import Alert, DomainError, SecurityEvent, Severity


class DetectionRule(Protocol):
    def evaluate(self, events: Iterable[SecurityEvent]) -> list[Alert]:
        ...


@dataclass(frozen=True)
class BruteForceRule:
    threshold: int = 5

    def __post_init__(self) -> None:
        if type(self.threshold) is not int or self.threshold < 1:
            raise DomainError("Seuil invalide")

    def evaluate(self, events: Iterable[SecurityEvent]) -> list[Alert]:
        counts = Counter(
            event.source_ip
            for event in events
            if event.action == "login_failed"
        )

        return [
            Alert("brute_force", ip, Severity.HIGH, "Tentatives SSH répétées")
            for ip, count in counts.items()
            if count >= self.threshold
        ]


class PortScanRule:
    def __init__(self, threshold: int = 20) -> None:
        if type(threshold) is not int or threshold < 1:
            raise DomainError("Seuil invalide")
        self.threshold = threshold

    def evaluate(self, events: Iterable[SecurityEvent]) -> list[Alert]:
        counts = Counter(
            event.source_ip
            for event in events
            if event.action == "port_probe"
        )

        return [
            Alert("port_scan", ip, Severity.MEDIUM, "Scan de ports détecté")
            for ip, count in counts.items()
            if count >= self.threshold
        ]


class RuleSet:
    def __init__(self, rules: Iterable[DetectionRule]) -> None:
        self.rules = tuple(rules)

    def evaluate(self, events: Iterable[SecurityEvent]) -> list[Alert]:
        event_list = list(events)
        alerts: list[Alert] = []

        for rule in self.rules:
            alerts.extend(rule.evaluate(event_list))

        return alerts


def build_rule(config: dict[str, object]) -> DetectionRule:
    kind = config.get("kind")
    threshold = config.get(
        "threshold",
        5 if kind == "brute_force" else 20
    )

    if type(threshold) is not int or threshold < 1:
        raise DomainError("Seuil invalide")

    if kind == "brute_force":
        return BruteForceRule(threshold)

    if kind == "port_scan":
        return PortScanRule(threshold)

    raise DomainError("Règle inconnue")
