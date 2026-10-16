
"""Tests de laboratoire : contrôle des autorisations."""

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_5_utilisateur_non_autorise() -> None:
    """Démontre qu'un utilisateur quelconque peut fermer un incident."""
    cursor = vuln.conn.execute(
        "INSERT INTO incident (ip, status) VALUES (?, ?)",
        ("192.0.2.50", "open"),
    )
    incident_id = cursor.lastrowid
    assert incident_id is not None

    vuln.close_incident("intrus", incident_id)

    result = vuln.conn.execute(
        "SELECT status FROM incident WHERE id = ?",
        (incident_id,),
    ).fetchone()

    assert result is not None
    assert result[0] == "closed"
