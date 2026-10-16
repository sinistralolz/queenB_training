
# ADR-0002 : Gestion des secrets par variables d'environnement

**Statut :** Accepté

**Contexte :** Queen Bee utilisait une clé API codée en dur, exposant un secret dans le code source.

**Décision :** Charger la clé depuis la variable d'environnement `QUEENBEE_LAB_API_KEY` et refuser son absence.

**Conséquences :** Aucun secret n'est nécessaire dans le dépôt. La configuration doit fournir la clé au démarrage ou avant son utilisation.

**Vérification :** `tests/test_lab_secret.py` valide l'absence de clé codée en dur et le comportement de chargement.
