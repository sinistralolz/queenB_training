
"""Tests de laboratoire : authentification inter-services."""

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_6_service_sans_authentification() -> None:
    """Démontre qu'un service peut être appelé sans identité vérifiée."""
    result = vuln.call_enrichment_service("192.0.2.10")

    assert result["ip"] == "192.0.2.10"
    assert result["reputation"] == "unknown"
