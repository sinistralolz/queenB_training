
# ADR-0006 : Contrôle des autorisations

**Statut :** Accepté

**Contexte :** La fermeture des incidents ne vérifiait pas les droits de l'utilisateur.

**Décision :** Vérifier le rôle avant toute fermeture d'incident. Seuls les rôles admin et analyst sont autorisés.

**Conséquences :** Les utilisateurs non autorisés reçoivent une erreur et l'incident reste ouvert. Le laboratoire simule les rôles en mémoire ; en production, ils doivent provenir d'une identité authentifiée.

**Vérification :** tests/test_lab_authorization.py vérifie le refus des utilisateurs non autorisés et l'accès des utilisateurs autorisés.
