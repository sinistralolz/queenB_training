
"""Tests de non-régression de la faille 4 : injection SQL."""

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_4_recherche_normale() -> None:
    """Une adresse IP connue retourne son incident."""
    vuln.conn.execute(
        "INSERT INTO incident (ip, status) VALUES (?, ?)",
        ("192.0.2.10", "open"),
    )

    result = vuln.find_incidents("192.0.2.10")

    assert result
    assert all(row[1] == "192.0.2.10" for row in result)


@pytest.mark.lab
def test_faille_4_injection_sql_bloquee() -> None:
    """Une injection SQL ne doit pas révéler les incidents."""
    vuln.conn.execute(
        "INSERT INTO incident (ip, status) VALUES (?, ?)",
        ("192.0.2.20", "open"),
    )

    result = vuln.find_incidents("x' OR '1'='1")

    assert result == []
