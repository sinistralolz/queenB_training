
# J3-A2 - Sauvegardes et plan de reprise d'activité

## 1. Objectif

Garantir la disponibilité des données de Queen Bee
et permettre une reprise du service après un incident.

## 2. Données à protéger

- Base SQLite contenant les incidents.
- Configuration de l'application.
- Règles de détection.
- Journaux de sécurité nécessaires aux investigations.
- Documentation et procédures d'exploitation.

Les secrets sont sauvegardés séparément,
avec des protections adaptées.

## 3. Objectifs de reprise

| Indicateur | Objectif cible | Signification |
|---|---|---|
| RPO | 1 heure | Perte maximale de données visée |
| RTO | 4 heures | Délai maximal de reprise visé |

Ces objectifs devront être validés par des tests.

## 4. Stratégie de sauvegarde

### Base de données

- Sauvegarde cohérente de SQLite toutes les heures.
- Utilisation de l'API de sauvegarde SQLite
  plutôt qu'une simple copie à chaud du fichier.
- Vérification de l'intégrité des sauvegardes.
- Conservation de plusieurs versions.

### Configuration

- Sauvegarde après chaque modification importante.
- Versionnement du code et des configurations
  non sensibles dans Git.
- Exclusion des secrets du dépôt Git.

### Journaux

- Centralisation vers un collecteur dédié.
- Conservation selon une durée définie.
- Protection contre la suppression non autorisée.

## 5. Règle 3-2-1

La stratégie cible repose sur :

- 3 copies des données.
- 2 types de supports ou emplacements distincts.
- 1 copie hors site.

Une copie isolée ou immuable est recommandée
pour limiter les conséquences d'un rançongiciel.

## 6. Plan de reprise d'activité

En cas d'incident majeur :

1. Identifier et contenir l'incident.
2. Isoler les systèmes compromis.
3. Préparer un environnement sain.
4. Restaurer la configuration et les données.
5. Vérifier l'intégrité de la base.
6. Tester les fonctionnalités de Queen Bee.
7. Réouvrir le service après validation.
8. Documenter l'incident et les actions réalisées.

## 7. Tests de restauration

Un test de restauration doit vérifier :

- La présence des données attendues.
- L'intégrité de la base SQLite.
- Le fonctionnement de l'application.
- Les contrôles d'accès.
- Le temps réel nécessaire à la reprise.

Le RPO et le RTO ne pourront être considérés
comme atteints qu'après des tests concluants.

## 8. Limites

Cette stratégie est une proposition pour
l'architecture cible de Queen Bee.

Les sauvegardes automatisées, la copie hors site
et les procédures de reprise restent à mettre
en œuvre et à tester.
