
# ADR 0009 - Sécurisation de l'infrastructure Queen Bee

## Statut

Proposé - J3-A2

## 1. Contexte

Queen Bee est une application de cybersécurité
chargée de recevoir des événements provenant
d'agents, de les analyser et de gérer des incidents.

Cette application traite des informations sensibles.

Une infrastructure insuffisamment protégée pourrait
permettre à un attaquant de compromettre les données,
d'usurper un agent ou de perturber le service.

Il est donc nécessaire de définir une architecture
réseau sécurisée.

## 2. Décision

Nous retenons une architecture cible reposant sur :

- La segmentation des zones réseau.
- Une DMZ pour le point d'entrée HTTPS.
- Une zone applicative pour les services internes.
- Une zone de données protégée.
- Une politique de filtrage deny all par défaut.
- L'authentification des agents et des services.
- La protection des secrets.
- La centralisation des journaux de sécurité.
- Une stratégie de sauvegarde et de reprise d'activité.

## 3. Justification des choix

### Segmentation réseau

La séparation des zones limite les déplacements
latéraux en cas de compromission.

Un agent compromis ne doit pas pouvoir accéder
directement à la base de données.

### Politique deny all

Les communications sont interdites par défaut.

Seuls les flux nécessaires au fonctionnement
de Queen Bee sont explicitement autorisés.

Cette approche réduit la surface d'attaque.

### Gestion des secrets

Les clés et jetons ne doivent pas être codés
en dur dans l'application.

Le laboratoire utilise des variables
d'environnement.

Un gestionnaire de secrets dédié est recommandé
pour un environnement de production.

### Journalisation et SIEM

Les événements de sécurité doivent être
centralisés afin de faciliter la détection
des attaques et les investigations.

Wazuh constitue une solution envisageable.

### Sauvegardes

Une stratégie de sauvegarde cohérente est
nécessaire pour protéger les incidents.

Objectifs proposés :

- RPO : 1 heure.
- RTO : 4 heures.

Ces objectifs devront être vérifiés
par des tests de restauration.

## 4. Solutions alternatives

### Infrastructure sans segmentation

Avantage :
- Déploiement plus simple.

Inconvénients :
- Surface d'attaque plus importante.
- Risque accru de déplacement latéral.

Cette solution n'est pas retenue.

### Base de données distante

Une base de données distante pourrait
être envisagée pour une architecture distribuée.

Cependant, Queen Bee utilise actuellement SQLite.

Une migration ajouterait de la complexité
et nécessiterait de nouveaux contrôles réseau.

Cette solution n'est pas retenue à ce stade.

### Absence de centralisation des journaux

Avantage :
- Moins de composants à administrer.

Inconvénients :
- Investigations plus difficiles.
- Risque de perte des traces.
- Détection moins efficace.

Cette solution n'est pas retenue
pour l'architecture cible.

## 5. Conséquences

### Avantages

- Réduction de la surface d'attaque.
- Meilleure protection des données.
- Limitation des déplacements latéraux.
- Amélioration de la traçabilité.
- Meilleure préparation aux incidents.

### Contraintes

- Configuration de règles réseau supplémentaires.
- Gestion des certificats et des secrets.
- Administration des journaux.
- Tests réguliers des sauvegardes.
- Maintenance de composants supplémentaires.

## 6. Limites

Cet ADR décrit une architecture cible.

La séparation physique ou logique des services,
les règles de pare-feu, le SIEM et les sauvegardes
automatisées ne sont pas considérés comme
déployés ou validés à ce stade.

Les ports réseau et les objectifs RPO/RTO
devront être confirmés lors de l'implémentation.

## 7. Documents associés

- docs/infrastructure/zones_reseau.md
- docs/infrastructure/matrice_flux.md
- docs/infrastructure/secrets_journalisation.md
- docs/infrastructure/sauvegardes_pra.md
- docs/threat_model.md
