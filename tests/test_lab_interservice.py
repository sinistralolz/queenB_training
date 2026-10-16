
"""Tests de non-régression : authentification inter-services."""

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_6_service_non_authentifie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("QUEENBEE_SERVICE_TOKEN", "secret-test-service")

    with pytest.raises(PermissionError):
        vuln.call_enrichment_service("192.0.2.10", "jeton-invalide")


@pytest.mark.lab
def test_faille_6_service_authentifie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("QUEENBEE_SERVICE_TOKEN", "secret-test-service")

    result = vuln.call_enrichment_service(
        "192.0.2.10",
        "secret-test-service",
    )

    assert result["ip"] == "192.0.2.10"
    assert result["reputation"] == "unknown"


@pytest.mark.lab
def test_faille_6_secret_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("QUEENBEE_SERVICE_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="non configuré"):
        vuln.call_enrichment_service("192.0.2.10", "jeton-test")
