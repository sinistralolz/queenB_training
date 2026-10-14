
from queenbee.application.services import DetectionService
from queenbee.config import Settings
from queenbee.domain.ports import AlertNotifier
from queenbee.domain.rules import BruteForceRule
from queenbee.factories import InMemoryFactory, ProdFactory


def bootstrap(settings: Settings, production: bool = False) -> DetectionService:
    """Assemble les composants sans utiliser de Singleton."""

    factory = (
        ProdFactory(settings.database_path)
        if production
        else InMemoryFactory()
    )

    repository = factory.repository()

    if production:
        raise NotImplementedError(
            "Le notificateur de production reste à configurer"
        )

    notifier: AlertNotifier = factory.notifier()

    return DetectionService(
        rule=BruteForceRule(),
        repository=repository,
        notifiers=[notifier],
    )
