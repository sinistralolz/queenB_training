
# ADR-0007 : Authentification inter-services

**Statut :** Accepté

**Contexte :** Le service d'enrichissement acceptait les appels sans authentification.

**Décision :** Exiger un jeton inter-services distinct de la clé API des agents, chargé depuis une variable d'environnement et comparé avec hmac.compare_digest().

**Conséquences :** Les appels avec un jeton incorrect sont refusés. En production, une protection TLS/mTLS et une gestion centralisée des secrets sont nécessaires.

**Vérification :** tests/test_lab_interservice.py vérifie les appels autorisés, refusés et l'absence de configuration.
