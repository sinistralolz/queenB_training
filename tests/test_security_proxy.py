
import pytest

from queenbee.application.security_proxy import (
    AccessDeniedError,
    IncidentReaderProxy,
)
from queenbee.adapters.outbound.repositories import (
    InMemoryIncidentRepository,
)


def test_abuse_unauthorized_user_cannot_read_incidents() -> None:
    """Un utilisateur sans rôle ne doit pas consulter les incidents."""

    repository = InMemoryIncidentRepository()
    proxy = IncidentReaderProxy(repository)

    with pytest.raises(AccessDeniedError):
        proxy.list_all(roles=[])


def test_viewer_can_read_incidents() -> None:
    """Un utilisateur viewer peut consulter les incidents."""

    repository = InMemoryIncidentRepository()
    proxy = IncidentReaderProxy(repository)

    incidents = proxy.list_all(roles=["viewer"])

    assert incidents == []
