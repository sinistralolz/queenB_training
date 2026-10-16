
# J3-A2 - Architecture réseau sécurisée de Queen Bee

## 1. Objectif

L'objectif est de segmenter l'infrastructure Queen Bee
afin de limiter les accès non autorisés et les déplacements
latéraux en cas de compromission.

## 2. Zones de sécurité

### Zone Agents
Machines qui collectent et transmettent les événements
de sécurité à Queen Bee.

### Zone DMZ
Héberge le point d'entrée HTTPS de l'API Queen Bee.
Elle contrôle les requêtes entrantes et leur authentification.

### Zone Applicative
Héberge les services internes chargés de traiter les
événements et de gérer les incidents.

### Zone Données
Contient la base de données des incidents.
Elle n'est pas directement accessible depuis les agents
ou Internet.

## 3. Principes de sécurité

- Segmentation entre les différentes zones.
- Pare-feu filtrant les communications interzones.
- Politique de refus par défaut.
- Autorisation des seuls flux nécessaires.
- Chiffrement TLS des communications réseau.
- Authentification des agents et des services.
- Journalisation des accès et des refus.

## 4. Exemple de scénario d'attaque

Si un agent est compromis, l'attaquant peut tenter
d'accéder aux autres composants de Queen Bee.

Grâce à la segmentation :
- L'agent peut uniquement contacter l'API autorisée.
- L'accès direct aux services internes est interdit.
- L'accès direct à la base de données est interdit.

Cette séparation réduit les possibilités de
déplacement latéral et limite l'impact d'une attaque.

## 5. Statut

Architecture cible proposée pour le projet J3-A2.
Les règles réseau restent à définir et à valider
dans la matrice des flux.
