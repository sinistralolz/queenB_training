
"""Configuration sécurisée de Queen Bee."""

import os
from collections.abc import Mapping
from dataclasses import dataclass, field

from queenbee.domain.model import DomainError


class ConfigError(DomainError):
    """Erreur de configuration de Queen Bee."""


@dataclass(frozen=True)
class Settings:
    """Paramètres de configuration de l'application."""

    database_path: str = ":memory:"
    agent_key: bytes = field(default=b"", repr=False)

    def __post_init__(self) -> None:
        if not self.database_path:
            raise ConfigError("Chemin de base de données invalide")

        if not isinstance(self.agent_key, bytes) or len(self.agent_key) < 32:
            raise ConfigError("Clé agent trop courte")


class SettingsBuilder:
    """Construit une configuration validée."""

    def __init__(self) -> None:
        self._database_path = ":memory:"
        self._agent_key: bytes | None = None

    def with_database(self, path: str) -> "SettingsBuilder":
        """Définit le chemin de la base de données."""

        self._database_path = path
        return self

    def hmac_key(self, key: bytes) -> "SettingsBuilder":
        """Définit la clé secrète HMAC."""

        self._agent_key = key
        return self

    def build(self) -> Settings:
        """Construit les paramètres après validation."""

        key = self._agent_key

        if key is None:
            raw_key = os.environ.get("QUEENBEE_AGENT_KEY", "")
            try:
                key = bytes.fromhex(raw_key)
            except ValueError as exc:
                raise ConfigError("Clé HMAC invalide") from exc

        return Settings(
            database_path=self._database_path,
            agent_key=key,
        )


def settings_from_env(env: Mapping[str, str]) -> Settings:
    """Charge et valide la configuration depuis des variables."""

    raw_key = env.get("QUEENBEE_AGENT_KEY", "")

    try:
        key = bytes.fromhex(raw_key)
    except ValueError as exc:
        raise ConfigError("Clé HMAC invalide") from exc

    return (
        SettingsBuilder()
        .with_database(env.get("QUEENBEE_DATABASE_PATH", ":memory:"))
        .hmac_key(key)
        .build()
    )
