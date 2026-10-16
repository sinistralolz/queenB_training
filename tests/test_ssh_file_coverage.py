
"""Tests complémentaires de lecture sécurisée des journaux SSH."""

from datetime import UTC, datetime

from queenbee.adapters.log_parser import read_ssh_failures


TIMESTAMP = datetime(2026, 10, 15, tzinfo=UTC)


def test_read_valid_ssh_failure(tmp_path):
    """Une ligne SSH valide est transformée en événement."""
    logfile = tmp_path / "auth.log"
    logfile.write_text(
        "Failed password for alice from 10.0.0.1\n",
        encoding="utf-8",
    )

    events = list(read_ssh_failures(logfile, TIMESTAMP))

    assert len(events) == 1
    assert events[0].username == "alice"
    assert events[0].source_ip == "10.0.0.1"


def test_read_empty_file(tmp_path):
    """Un fichier vide ne produit aucun événement."""
    logfile = tmp_path / "empty.log"
    logfile.write_text("", encoding="utf-8")

    assert list(read_ssh_failures(logfile, TIMESTAMP)) == []


def test_read_ignores_invalid_lines(tmp_path):
    """Les lignes invalides sont ignorées."""
    logfile = tmp_path / "invalid.log"
    logfile.write_text(
        "Ceci n'est pas un journal SSH\n"
        "Failed password for alice from 10.0.0.1\n"
        "Failed password for bob from 999.999.999.999\n"
        "Failed password for charlie from 10.0.0.2\n",
        encoding="utf-8",
    )

    events = list(read_ssh_failures(logfile, TIMESTAMP))

    assert len(events) == 2
    assert [event.username for event in events] == ["alice", "charlie"]


def test_read_skips_oversized_line_and_continues(tmp_path):
    """Une ligne trop longue est ignorée sans perdre la suivante."""
    logfile = tmp_path / "oversized.log"
    logfile.write_text(
        ("X" * 5000)
        + "\n"
        + "Failed password for alice from 10.0.0.1\n",
        encoding="utf-8",
    )

    events = list(read_ssh_failures(logfile, TIMESTAMP))

    assert len(events) == 1
    assert events[0].username == "alice"


def test_read_skips_oversized_line_ending_at_eof(tmp_path):
    """Une ligne trop longue sans retour à la ligne est ignorée."""
    logfile = tmp_path / "oversized_eof.log"
    logfile.write_text("X" * 5000, encoding="utf-8")

    assert list(read_ssh_failures(logfile, TIMESTAMP)) == []


def test_read_rejects_null_byte(tmp_path):
    """Une ligne contenant un caractère nul est rejetée."""
    logfile = tmp_path / "null.log"
    logfile.write_text(
        "Failed password for alice from 10.0.0.1\x00\n",
        encoding="utf-8",
    )

    assert list(read_ssh_failures(logfile, TIMESTAMP)) == []


def test_read_accepts_windows_line_endings(tmp_path):
    """Les fins de ligne Windows sont acceptées."""
    logfile = tmp_path / "windows.log"
    logfile.write_bytes(
        b"Failed password for alice from 10.0.0.1\r\n"
    )

    events = list(read_ssh_failures(logfile, TIMESTAMP))

    assert len(events) == 1
    assert events[0].username == "alice"
