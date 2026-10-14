
"""Tests de caractérisation du comportement de détection SSH."""

from queenbee.domain.rules import BruteForceRule
from tests.conftest import ev


def test_five_failed_logins_trigger_alert():
    """Cinq échecs depuis la même IP déclenchent une alerte."""
    events = [
        ev(ip="10.0.0.1", action="login_failed")
        for _ in range(5)
    ]

    alerts = BruteForceRule(5).evaluate(events)

    assert len(alerts) == 1
    assert alerts[0].rule == "brute_force"
    assert alerts[0].source_ip == "10.0.0.1"


def test_four_failed_logins_do_not_trigger_alert():
    """Quatre échecs depuis la même IP ne déclenchent pas d'alerte."""
    events = [
        ev(ip="10.0.0.1", action="login_failed")
        for _ in range(4)
    ]

    alerts = BruteForceRule(5).evaluate(events)

    assert alerts == []
