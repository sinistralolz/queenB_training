
import os
from dataclasses import dataclass, field

from queenbee.domain.model import DomainError


@dataclass(frozen=True)
class Settings:
    database_path: str
    agent_key: str = field(repr=False)

    def __post_init__(self) -> None:
        if not self.database_path:
            raise DomainError("Chemin de base de données invalide")

        if len(self.agent_key) < 32:
            raise DomainError("Clé agent trop courte")


class SettingsBuilder:
    def __init__(self) -> None:
        self._database_path = ":memory:"

    def with_database(self, path: str) -> "SettingsBuilder":
        self._database_path = path
        return self

    def build(self) -> Settings:
        agent_key = os.environ.get("QUEENBEE_AGENT_KEY", "")

        return Settings(
            database_path=self._database_path,
            agent_key=agent_key,
        )
