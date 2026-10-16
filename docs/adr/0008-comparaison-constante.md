
# ADR-0008 : Comparaison sécurisée des jetons

**Statut :** Accepté

**Contexte :** La vérification des jetons utilisait l'opérateur ==, qui n'offre pas de garantie de comparaison en temps constant.

**Décision :** Utiliser hmac.compare_digest() pour comparer les jetons d'authentification.

**Conséquences :** Le risque de fuite d'information lié au temps de comparaison est réduit. La protection des secrets reste nécessaire.

**Vérification :** tests/test_lab_timing.py contrôle l'utilisation de compare_digest et le comportement avec des jetons valides et invalides.
