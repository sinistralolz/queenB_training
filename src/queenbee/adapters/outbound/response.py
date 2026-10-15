
"""Commandes sécurisées de réponse aux incidents."""

from dataclasses import dataclass, field
from ipaddress import ip_address


@dataclass(frozen=True)
class BlockIpCommand:
    """Commande de blocage d'une adresse IP validée."""

    ip: str

    def __post_init__(self) -> None:
        try:
            ip_address(self.ip)
        except ValueError as exc:
            raise ValueError("Adresse IP invalide") from exc


class InMemoryFirewall:
    """Simule un pare-feu sans modifier le réseau réel."""

    def __init__(self) -> None:
        self.blocked_ips: set[str] = set()

    def block(self, command: BlockIpCommand) -> None:
        self.blocked_ips.add(command.ip)

    def unblock(self, command: BlockIpCommand) -> None:
        self.blocked_ips.discard(command.ip)


@dataclass
class CommandHistory:
    """Conserve l'historique des commandes exécutées."""

    commands: list[BlockIpCommand] = field(default_factory=list)

    def execute(
        self,
        command: BlockIpCommand,
        firewall: InMemoryFirewall,
    ) -> None:
        firewall.block(command)
        self.commands.append(command)

    def undo(self, firewall: InMemoryFirewall) -> None:
        if not self.commands:
            return

        command = self.commands.pop()
        firewall.unblock(command)
