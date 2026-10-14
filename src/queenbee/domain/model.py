
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from ipaddress import ip_address
import re


class DomainError(ValueError):
    """Erreur lorsqu'une règle métier n'est pas respectée."""


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(Enum):
    OPEN = "open"
    TRIAGED = "triaged"
    CLOSED = "closed"


@dataclass(frozen=True)
class SecurityEvent:
    source_ip: str
    username: str
    action: str
    timestamp: datetime

    def __post_init__(self) -> None:
        try:
            ip_address(self.source_ip)
        except ValueError as exc:
            raise DomainError("Adresse IP invalide") from exc

        if not isinstance(self.username, str) or not re.fullmatch(
            r"[a-zA-Z0-9_.-]{1,64}", self.username
        ):
            raise DomainError("Nom d'utilisateur invalide")

        if self.action not in {"login_failed", "login_ok", "port_probe"}:
            raise DomainError("Action non autorisée")

        if not isinstance(self.timestamp, datetime) or (
            self.timestamp.tzinfo is None
            or self.timestamp.utcoffset() is None
        ):
            raise DomainError("Date sans fuseau horaire")


@dataclass(frozen=True)
class Alert:
    rule: str
    source_ip: str
    severity: Severity
    message: str


class Incident:
    def __init__(self, alert: Alert) -> None:
        self.alert = alert
        self.status = IncidentStatus.OPEN

    def transition_to(self, new_status: IncidentStatus) -> None:
        allowed = {
            IncidentStatus.OPEN: {IncidentStatus.TRIAGED},
            IncidentStatus.TRIAGED: {IncidentStatus.CLOSED},
            IncidentStatus.CLOSED: set(),
        }

        if new_status not in allowed[self.status]:
            raise DomainError("Transition d'incident interdite")

        self.status = new_status
