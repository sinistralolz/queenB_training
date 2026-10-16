
"""Tests complémentaires du contrôle d'accès aux incidents."""

import pytest

from queenbee.application.access import IncidentReadProxy
from queenbee.application.services import AccessDeniedError
from queenbee.domain.model import Principal


class FakeRepository:
    """Simule un dépôt capable de lister les incidents ouverts."""

    def list_open(self) -> list:
        return []


@pytest.mark.parametrize("role", ["viewer", "analyst", "admin"])
def test_authorized_roles_can_list_incidents(role: str) -> None:
    """Les trois rôles autorisés peuvent consulter les incidents."""
    principal = Principal(
        username="alice",
        roles=frozenset({role}),
    )
    proxy = IncidentReadProxy(FakeRepository(), principal)

    assert proxy.list_open() == []


def test_unauthorized_role_is_rejected() -> None:
    """Un utilisateur sans rôle autorisé est refusé."""
    principal = Principal(
        username="bob",
        roles=frozenset({"guest"}),
    )
    proxy = IncidentReadProxy(FakeRepository(), principal)

    with pytest.raises(AccessDeniedError):
        proxy.list_open()


def test_repository_without_list_open_is_rejected() -> None:
    """Un dépôt incompatible provoque une erreur explicite."""
    principal = Principal(
        username="alice",
        roles=frozenset({"analyst"}),
    )
    proxy = IncidentReadProxy(object(), principal)

    with pytest.raises(TypeError, match="Le dépôt ne permet pas"):
        proxy.list_open()
