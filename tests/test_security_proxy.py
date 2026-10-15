
import pytest

from queenbee.adapters.outbound.repositories import InMemoryIncidentRepository
from queenbee.application.security_proxy import (
    AccessDeniedError,
    IncidentReaderProxy,
)


class SpyIncidentRepository(InMemoryIncidentRepository):
    """Compte les consultations du dépôt."""

    def __init__(self) -> None:
        super().__init__()
        self.read_count = 0

    def list_all(self):
        self.read_count += 1
        return super().list_all()


def test_abuse_unauthorized_user_cannot_read_incidents() -> None:
    repository = SpyIncidentRepository()
    proxy = IncidentReaderProxy(repository)

    with pytest.raises(AccessDeniedError):
        proxy.list_all(roles=[])

    assert repository.read_count == 0


def test_viewer_can_read_incidents() -> None:
    repository = SpyIncidentRepository()
    proxy = IncidentReaderProxy(repository)
