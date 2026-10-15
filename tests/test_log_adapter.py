
from datetime import datetime, timezone

import pytest

from queenbee.adapters.log_parser import parse_ssh_failure


TIMESTAMP = datetime(2026, 10, 15, tzinfo=timezone.utc)


def test_valid_ssh_log_is_accepted() -> None:
    line = "Failed password for admin from 10.0.0.1"

    event = parse_ssh_failure(line, TIMESTAMP)

    assert event is not None
    assert event.source_ip == "10.0.0.1"
    assert event.username == "admin"
    assert event.action == "login_failed"


@pytest.mark.parametrize(
    "line",
    [
        "A" * 10000,
        "Failed password for admin from 10.0.0.1\x00",
        "Failed password for admin from 10.0.0.1; rm -rf /",
        "Failed password for admin from 999.999.999.999",
        " Failed password for admin from 10.0.0.1",
        "Failed password for admin from 10.0.0.1\nINJECTED",
    ],
)
def test_abuse_malicious_ssh_logs_are_rejected(line: str) -> None:
    """Les lignes malveillantes ne doivent produire aucun événement."""

    event = parse_ssh_failure(line, TIMESTAMP)

    assert event is None
