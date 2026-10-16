
# Queen Bee - Matrice de traçabilité exigences / tests

## 1. Objectif

Associer chaque exigence importante du projet
à un contrôle ou à un test permettant de vérifier
son bon fonctionnement.

## 2. Exigences fonctionnelles et techniques

| ID | Exigence | Vérification |
|---|---|---|
| EX-01 | Recevoir les événements des agents | Tests de l'API agent |
| EX-02 | Analyser les événements de sécurité | Tests des règles métier |
| EX-03 | Gérer les incidents | Tests des services applicatifs |
| EX-04 | Enregistrer les incidents | Tests des repositories |
| EX-05 | Respecter l'architecture hexagonale | lint-imports |
| EX-06 | Maintenir une couverture >= 90 % | pytest-cov |

## 3. Exigences de sécurité

| ID | Exigence | Test associé |
|---|---|---|
| SEC-01 | Ne pas coder les secrets en dur | tests/test_lab_secret.py |
| SEC-02 | Éviter les ReDoS | tests/test_lab_redos.py |
| SEC-03 | Empêcher la désérialisation dangereuse | tests/test_lab_pickle.py |
| SEC-04 | Empêcher les injections SQL | tests/test_lab_sql.py |
| SEC-05 | Contrôler les autorisations | tests/test_lab_authorization.py |
| SEC-06 | Authentifier les appels interservices | tests/test_lab_interservice.py |
| SEC-07 | Comparer les jetons de manière sécurisée | tests/test_lab_timing.py |

## 4. Vérifications automatiques

| Outil | Objectif | Dernier résultat |
|---|---|---|
| Ruff | Qualité et formatage | Validé |
| mypy | Vérification des types | Validé |
| pytest | Tests automatisés | 102 réussis |
| pytest-cov | Couverture du code | 90,37 % |
| Bandit | Analyse statique de sécurité | Validé sur src |
| lint-imports | Contrôle des dépendances | 1 contrat respecté |
| pip-audit | Audit des dépendances | À compléter |

## 5. Tests historiques des vulnérabilités

Le fichier tests/test_lab_vulnerable.py
contient trois tests de démonstration.

Ces tests cherchent à prouver l'existence
des vulnérabilités initiales.

Après correction, leurs conditions ne sont
plus satisfaites.

Ils sont conservés comme éléments pédagogiques,
mais exclus de la suite de validation finale.

## 6. Limites

La présence d'un test ne garantit pas
à elle seule la sécurité de l'application.

Les contrôles doivent être complétés par
des revues de code, des audits et des tests
d'intégration adaptés à l'environnement réel.
