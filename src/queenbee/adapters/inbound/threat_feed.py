
"""Traduction sécurisée des données de menaces externes."""

from dataclasses import dataclass
from ipaddress import ip_address

from queenbee.domain.model import DomainError


@dataclass(frozen=True)
class ThreatIndicator:
    """Indicateur de menace validé."""

    indicator: str
    score: int


class ThreatFeedTranslator:
    """Convertit les données externes en indicateurs fiables."""

    RISK_SCORES = {
        "low": 20,
        "medium": 50,
        "high": 80,
        "critical": 100,
    }

    def translate(self, data: dict[str, str]) -> ThreatIndicator:
        """Valide l'indicateur et traduit son niveau de risque."""

        if not isinstance(data, dict):
            raise DomainError("Données de menace invalides")

        if set(data) != {"indicator", "risk_level"}:
            raise DomainError("Champs de menace invalides")

        indicator = data["indicator"]
        risk_level = data["risk_level"]

        if not isinstance(indicator, str):
            raise DomainError("Indicateur invalide")

        try:
            ip_address(indicator)
        except ValueError as exc:
            raise DomainError("L'indicateur doit être une adresse IP") from exc

        if not isinstance(risk_level, str) or risk_level not in self.RISK_SCORES:
            raise DomainError("Niveau de risque inconnu")

        return ThreatIndicator(
            indicator=indicator,
            score=self.RISK_SCORES[risk_level],
        )
