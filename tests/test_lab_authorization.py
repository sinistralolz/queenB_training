
"""Tests de non-régression : autorisations."""

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_5_utilisateur_non_autorise() -> None:
    """Un utilisateur sans droits ne peut pas fermer un incident."""
    cursor = vuln.conn.execute(
        "INSERT INTO incident (ip, status) VALUES (?, ?)",
        ("192.0.2.50", "open"),
    )
    incident_id = cursor.lastrowid
    assert incident_id is not None

    with pytest.raises(PermissionError):
        vuln.close_incident("intrus", incident_id)

    result = vuln.conn.execute(
        "SELECT status FROM incident WHERE id = ?",
        (incident_id,),
    ).fetchone()

    assert result is not None
    assert result[0] == "open"


@pytest.mark.lab
@pytest.mark.parametrize("user", ["administrateur", "analyste"])
def test_faille_5_utilisateur_autorise(user: str) -> None:
    """Un administrateur ou analyste peut fermer un incident."""
    cursor = vuln.conn.execute(
        "INSERT INTO incident (ip, status) VALUES (?, ?)",
        ("192.0.2.60", "open"),
    )
    incident_id = cursor.lastrowid
    assert incident_id is not None

    vuln.close_incident(user, incident_id)

    result = vuln.conn.execute(
        "SELECT status FROM incident WHERE id = ?",
        (incident_id,),
    ).fetchone()

    assert result is not None
    assert result[0] == "closed"
