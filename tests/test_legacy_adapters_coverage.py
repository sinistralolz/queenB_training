
"""Tests complémentaires des adaptateurs SMTP et SQLite."""

import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from queenbee.adapters.email_notifier import EmailNotifier
from queenbee.adapters.sqlite_repository import SQLiteIncidentRepository
from queenbee.domain.model import Alert, Incident, Severity


def make_alert() -> Alert:
    """Crée une alerte pour les tests."""
    return Alert(
        rule="ssh_bruteforce",
        source_ip="10.0.0.66",
        severity=Severity.HIGH,
        message="Tentatives de connexion suspectes",
    )


def test_email_notifier_requires_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Refuse l'envoi si le mot de passe SMTP est absent."""
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)

    notifier = EmailNotifier()

    with pytest.raises(ValueError, match="SMTP_PASSWORD"):
        notifier.send(make_alert())


def test_email_notifier_sends_secure_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Utilise TLS et une authentification pour envoyer l'alerte."""
    monkeypatch.setenv("SMTP_PASSWORD", "test-password")

    smtp = MagicMock()
    smtp_context = MagicMock()
    smtp_context.__enter__.return_value = smtp

    with patch(
        "queenbee.adapters.email_notifier.smtplib.SMTP",
        return_value=smtp_context,
    ) as smtp_factory:
        notifier = EmailNotifier(
            host="smtp.example.test",
            port=587,
            username="queenbee",
        )
        notifier.send(make_alert())

    smtp_factory.assert_called_once_with(
        "smtp.example.test",
        587,
        timeout=10,
    )
    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once_with("queenbee", "test-password")
    smtp.send_message.assert_called_once()

    message = smtp.send_message.call_args.args[0]
    assert message["To"] == "soc@local"
    assert "10.0.0.66" in message.get_content()


def test_sqlite_repository_saves_incident(tmp_path) -> None:
    """Enregistre un incident dans une base SQLite temporaire."""
    db_path = tmp_path / "incidents.db"
    repository = SQLiteIncidentRepository(str(db_path))

    incident = Incident(alert=make_alert())
    repository.save(incident)

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "SELECT source_ip, rule, severity, status FROM incidents"
        ).fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "10.0.0.66"
    assert rows[0][1] == "ssh_bruteforce"
    assert rows[0][2] == Severity.HIGH.value
    assert rows[0][3] == incident.status.value
