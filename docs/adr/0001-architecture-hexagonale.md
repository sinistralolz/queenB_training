# ADR 0001 — Choix d'une architecture hexagonale pour Queen Bee

- **Statut** : accepté
- **Décideurs** : équipe de développement Queen Bee

## Contexte

Queen Bee est un outil de cybersécurité qui analyse des événements, détecte des comportements suspects et permet de gérer des incidents.

Le projet doit pouvoir recevoir des événements depuis différentes sources, utiliser plusieurs règles de détection et enregistrer les incidents sans dépendre d'une technologie unique.

Il faut également protéger les données contre les entrées malveillantes et faciliter les tests.

## Décision

Nous choisissons une **architecture hexagonale (Ports & Adapters)**.

Le projet est organisé en plusieurs parties :

- **Domain** : contient les objets métier, les règles de détection et les transitions d'état des incidents.
- **Application** : contient les services et les cas d'utilisation.
- **Adapters** : assurent les échanges avec l'extérieur, notamment les journaux SSH, les notifications et les bases de données.
- **Bootstrap** : assemble les différents composants.

Le domaine ne doit pas dépendre des adaptateurs techniques.

Les communications avec les composants externes passent par des interfaces (ports), ce qui permet de remplacer une implémentation sans modifier la logique métier.

## Alternatives écartées

**1. Architecture monolithique sans séparation claire**

Cette solution serait plus rapide à développer au départ, mais elle mélangerait les règles métier, la gestion des données et les interactions externes.

Cela compliquerait les tests et les évolutions du projet.

**2. Architecture microservices**

Elle permettrait de séparer les composants en plusieurs services indépendants.

Cependant, elle nécessiterait davantage de déploiements, de communications réseau, de supervision et de mécanismes de sécurité.

Pour la taille actuelle de Queen Bee, cette complexité supplémentaire n'est pas justifiée.

## Conséquences

**Avantages :**

- Les règles de détection peuvent être testées indépendamment.
- Les adaptateurs peuvent être remplacés plus facilement.
- Les responsabilités sont mieux séparées.
- Les tests peuvent utiliser des composants simulés, sans base de données ni réseau réel.
- Les contrôles de sécurité peuvent être placés aux frontières du système.

**Inconvénients :**

- Le projet comporte davantage de fichiers et d'interfaces.
- L'organisation demande plus de rigueur.
- Certaines fonctionnalités simples nécessitent plusieurs composants.

## Menaces STRIDE traitées

| Menace | Mesure prévue dans Queen Bee |
|---|---|
| Spoofing (usurpation d'identité) | Vérification HMAC des messages envoyés par les agents |
| Tampering (modification de données) | Validation des événements et des transitions d'incidents |
| Repudiation (répudiation) | Journalisation des actions sensibles |
| Information Disclosure (divulgation) | Contrôle des accès avec le pattern Proxy |
| Denial of Service (déni de service) | Limitation des alertes avec le pattern Decorator |
| Elevation of Privilege (élévation de privilèges) | Vérification des autorisations avant les opérations sensibles |

Ces protections doivent être vérifiées par des tests. Certaines, notamment la vérification HMAC et les autorisations des services applicatifs, seront finalisées pendant l'A3.

## Preuve

Les tests réalisés pendant l'A1 vérifient notamment :

- Le refus d'accès aux incidents pour un rôle non autorisé.
- La limitation de 1 000 alertes à 3 notifications transmises.
- Le rejet de journaux SSH malformés ou malveillants.
- La transmission des notifications à plusieurs abonnés.
- Le rejet d'une injection de commande dans une adresse IP.
- L'annulation d'un blocage IP.

**Résultats constatés :**

- 36 tests réussis sur les parties déjà développées.
- Ruff : aucune erreur.
- Mypy : aucune erreur sur 18 fichiers.

**Preuves complémentaires attendues à l'A3 :**

- Tests des signatures HMAC invalides.
- Tests des autorisations des services applicatifs.
- Vérification automatique des dépendances entre les couches.
- Validation de l'ensemble du projet avec `make check`.

## Comparaison : architecture hexagonale et microservices

| Critère | Architecture hexagonale | Microservices |
|---|---|---|
| Organisation | Séparation entre domaine, application et adaptateurs | Plusieurs services indépendants |
| Déploiement | Une seule application peut suffire | Chaque service peut être déployé séparément |
| Communication | Principalement des appels internes | Souvent des appels réseau ou des messages |
| Tests | Tests unitaires facilités par les ports | Tests d'intégration distribués plus complexes |
| Sécurité | Contrôles aux frontières et dans les services | Contrôles supplémentaires entre les services |
| Maintenance | Adaptée à une application de taille modérée | Utile pour plusieurs équipes ou composants autonomes |
| Complexité | Modérée | Plus élevée |

### Choix pour Queen Bee

Nous retenons l'architecture hexagonale, car Queen Bee est encore un projet de taille limitée.

Elle permet de séparer les règles de détection des composants techniques sans ajouter la complexité de plusieurs services à déployer et à sécuriser.

Cette organisation permet notamment de remplacer un stockage en mémoire par SQLite, ou de modifier le système de notification, sans devoir réécrire les règles métier.

Les microservices pourraient devenir intéressants si Queen Bee devait gérer plusieurs composants indépendants à grande échelle.

**Ces deux approches ne sont pas incompatibles :** un microservice peut lui-même utiliser une architecture hexagonale.

Pour Queen Bee, nous privilégions donc une application simple à déployer, mais dont les composants internes restent indépendants et testables.
