
"""Commandes sécurisées de réponse aux incidents."""

from dataclasses import dataclass, field
from ipaddress import ip_address


@dataclass(frozen=True, init=False)
class BlockIpCommand:
    """Commande de blocage d'une adresse IP validée."""

    ip: str
    firewall: "InMemoryFirewall | None"

    def __init__(
        self,
        ip_or_firewall: str | "InMemoryFirewall",
        ip: str | None = None,
    ) -> None:
        """Accepte BlockIpCommand(ip) ou BlockIpCommand(firewall, ip)."""

        if isinstance(ip_or_firewall, InMemoryFirewall):
            firewall = ip_or_firewall
            address = ip
        else:
            firewall = None
            address = ip_or_firewall

        if not isinstance(address, str):
            raise ValueError("IP address does not appear to be valid")

        try:
            ip_address(address)
        except ValueError as exc:
            raise ValueError(
                "IP address does not appear to be valid"
            ) from exc

        object.__setattr__(self, "ip", address)
        object.__setattr__(self, "firewall", firewall)


class InMemoryFirewall:
    """Simule un pare-feu sans modifier le réseau réel."""

    def __init__(self) -> None:
        self.blocked_ips: set[str] = set()

    @property
    def blocked(self) -> set[str]:
        """Retourne les adresses IP bloquées."""
        return self.blocked_ips

    def block(self, command: BlockIpCommand) -> None:
        """Bloque une adresse IP."""
        self.blocked_ips.add(command.ip)

    def unblock(self, command: BlockIpCommand) -> None:
        """Débloque une adresse IP."""
        self.blocked_ips.discard(command.ip)


@dataclass
class CommandHistory:
    """Conserve l'historique des commandes exécutées."""

    commands: list[BlockIpCommand] = field(default_factory=list)
    _firewalls: list[InMemoryFirewall] = field(default_factory=list)

    def execute(
        self,
        command: BlockIpCommand,
        firewall: InMemoryFirewall,
    ) -> None:
        """Exécute une commande avec un pare-feu explicite."""

        firewall.block(command)
        self.commands.append(command)
        self._firewalls.append(firewall)

    def undo(self, firewall: InMemoryFirewall) -> None:
        """Annule la dernière commande exécutée."""

        if not self.commands:
            return

        command = self.commands.pop()
        self._firewalls.pop()
        firewall.unblock(command)

    def run(self, command: BlockIpCommand) -> None:
        """Exécute une commande contenant son propre pare-feu."""

        if command.firewall is None:
            raise ValueError("Pare-feu manquant")

        self.execute(command, command.firewall)

    def undo_last(self) -> None:
        """Annule la dernière commande avec son pare-feu associé."""

        if not self.commands:
            return

        firewall = self._firewalls[-1]
        self.undo(firewall)
