
import pytest

from queenbee.adapters.outbound.response import (
    BlockIpCommand,
    CommandHistory,
    InMemoryFirewall,
)


def test_valid_ip_can_be_blocked() -> None:
    """Une adresse IP valide peut être bloquée."""

    firewall = InMemoryFirewall()
    history = CommandHistory()
    command = BlockIpCommand("192.168.1.10")

    history.execute(command, firewall)

    assert "192.168.1.10" in firewall.blocked_ips
    assert history.commands == [command]


def test_abuse_command_injection_is_rejected() -> None:
    """Une injection de commande doit être refusée."""

    firewall = InMemoryFirewall()

    with pytest.raises(ValueError):
        BlockIpCommand("1.2.3.4; iptables -F")

    # Aucun blocage ne doit avoir été effectué.
    assert firewall.blocked_ips == set()


def test_abuse_invalid_ip_is_rejected() -> None:
    """Une adresse IP invalide doit être refusée."""

    with pytest.raises(ValueError):
        BlockIpCommand("999.999.999.999")


def test_command_can_be_undone() -> None:
    """Un blocage peut être annulé."""

    firewall = InMemoryFirewall()
    history = CommandHistory()
    command = BlockIpCommand("10.0.0.5")

    history.execute(command, firewall)

    assert "10.0.0.5" in firewall.blocked_ips

    history.undo(firewall)

    assert "10.0.0.5" not in firewall.blocked_ips
    assert history.commands == []
