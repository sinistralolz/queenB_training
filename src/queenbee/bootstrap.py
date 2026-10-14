
from queenbee.adapters.outbound.notifiers import MemoryNotifier
from queenbee.application.services import DetectionService
from queenbee.config import Settings
from queenbee.domain.rules import BruteForceRule
from queenbee.factories import InMemoryFactory, ProdFactory


def bootstrap(settings: Settings, production: bool = False) -> DetectionService:
    """Assemble les composants sans utiliser de Singleton."""

    if production:
        factory = ProdFactory(settings.database_path)
    else:
        factory = InMemoryFactory()

    repository = factory.repository()

    if production:
        raise NotImplementedError(
            "Le notificateur de production reste à configurer"
        )

    notifier: MemoryNotifier = factory.notifier()

    return DetectionService(
        rule=BruteForceRule(),
        repository=repository,
        notifiers=[notifier],
    )
