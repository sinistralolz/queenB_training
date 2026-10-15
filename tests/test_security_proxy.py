
import pytest

from queenbee.adapters.outbound.repositories import InMemoryIncidentRepository
from queenbee.application.security_proxy import (
    AccessDeniedError,
    IncidentReaderProxy,
)
from queenbee.domain.model import Incident


class SpyIncidentRepository(InMemoryIncidentRepository):
    """Compte les consultations du dépôt."""

    def __init__(self) -> None:
        super().__init__()
        self.read_count = 0

    def list_all(self) -> list[Incident]:
        self.read_count += 1
        return super().list_all()


def test_abuse_unauthorized_user_cannot_read_incidents() -> None:
    repository = SpyIncidentRepository()
    proxy = IncidentReaderProxy(repository, roles=[])

    with pytest.raises(AccessDeniedError):
        proxy.list_all()

    assert repository.read_count == 0


def test_viewer_can_read_incidents() -> None:
    repository = SpyIncidentRepository()
    proxy = IncidentReaderProxy(repository, roles=["viewer"])

    assert proxy.list_all() == []
    assert repository.read_count == 1


def test_analyst_can_read_incidents() -> None:
    repository = SpyIncidentRepository()
    proxy = IncidentReaderProxy(repository, roles=["analyst"])

    assert proxy.list_all() == []
    assert repository.read_count == 1
