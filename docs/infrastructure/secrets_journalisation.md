
# J3-A2 - Gestion des secrets et journalisation

## 1. Objectif

Protéger les informations sensibles de Queen Bee
et assurer la traçabilité des événements de sécurité.

## 2. Gestion des secrets

Les secrets comprennent notamment :
- Les clés API des agents.
- Les jetons d'authentification interservices.
- Les identifiants des services externes.
- Les éventuels identifiants d'administration.

### Mesures de sécurité

- Aucun secret ne doit être écrit en dur dans le code.
- Les secrets ne doivent pas être enregistrés dans Git.
- Les accès aux secrets suivent le moindre privilège.
- Les secrets doivent pouvoir être renouvelés.
- Les journaux ne doivent jamais contenir de secrets.

### Stockage

Pour le laboratoire, les variables d'environnement
permettent de fournir les secrets à l'application.

En production, un gestionnaire de secrets dédié
serait préférable.

Les variables d'environnement ne constituent pas
à elles seules un coffre-fort sécurisé.

## 3. Journalisation

Queen Bee doit permettre de tracer :

- Les tentatives d'authentification.
- Les accès refusés.
- La réception des événements des agents.
- La création et la clôture des incidents.
- Les erreurs applicatives.
- Les anomalies de sécurité.

Chaque journal doit idéalement contenir :

- Un horodatage UTC.
- Un identifiant de service.
- Un identifiant d'acteur si disponible.
- Le type d'événement.
- Le résultat de l'opération.
- Un identifiant de corrélation.

Les journaux ne doivent pas exposer les clés API,
les jetons ou les mots de passe.

## 4. Centralisation des journaux

Architecture cible :

Queen Bee
    |
    | Journaux applicatifs
    v
Collecteur de journaux
    |
    | Transport chiffré
    v
SIEM (exemple : Wazuh)
    |
    v
Alertes de sécurité

Le SIEM permet de corréler les événements,
détecter les comportements suspects
et faciliter les investigations.

## 5. Exemples d'alertes

### Tentatives d'authentification répétées

Plusieurs refus d'authentification provenant
d'une même source peuvent déclencher une alerte.

### Accès non autorisé

Une tentative de clôture d'incident par un
utilisateur non habilité doit être journalisée.

### Volume anormal d'événements

Une augmentation brutale du nombre d'événements
peut signaler un dysfonctionnement ou une attaque.

## 6. Protection des journaux

- Accès limité aux administrateurs et analystes habilités.
- Transmission chiffrée vers le collecteur.
- Protection contre la modification et la suppression.
- Politique de conservation définie.
- Synchronisation horaire des systèmes.

## 7. Limites

Ce document présente des mesures de sécurité
et une architecture cible.

La centralisation SIEM, la rotation automatique
des secrets et les alertes décrites doivent
être déployées et testées avant de pouvoir
être considérées comme opérationnelles.
