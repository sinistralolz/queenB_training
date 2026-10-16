
# J3-A2 - Matrice des flux réseau Queen Bee

## 1. Objectif

Définir les communications autorisées entre les zones
de sécurité de Queen Bee.

Principe : tout flux non explicitement autorisé
est interdit par défaut (deny all).

## 2. Matrice des flux

| Source | Destination | Protocole / Port | Décision | Justification |
|---|---|---|---|---|
| Agents | API Queen Bee (DMZ) | HTTPS / TCP 443 | Autorisé | Transmission sécurisée des événements |
| API Queen Bee | Service applicatif | HTTPS / TCP 8443 | Autorisé | Traitement interne des événements |
| Service applicatif | Base SQLite locale | Accès fichier, pas de port réseau | Autorisé sous conditions | Lecture et écriture des incidents |
| Agents | Service applicatif | Tous | Interdit | Empêcher le contournement de l'API |
| Agents | Base de données | Tous | Interdit | Protéger les incidents |
| Internet | Service applicatif | Tous | Interdit | Limiter la surface d'attaque |
| Internet | Base de données | Tous | Interdit | Empêcher l'accès direct aux données |
| DMZ | Réseau d'administration | Tous | Interdit | Empêcher les déplacements latéraux |

## 3. Risques STRIDE

### Spoofing (usurpation d'identité)
Risque : un faux agent tente de transmettre des événements.

Mesures :
- Authentification des agents.
- Vérification des jetons.
- TLS pour protéger les communications.

### Tampering (altération)
Risque : modification des événements pendant leur transmission.

Mesures :
- TLS.
- Validation des données reçues.
- Contrôle des droits d'écriture.

### Repudiation (répudiation)
Risque : impossibilité de retrouver l'origine d'une action.

Mesures :
- Journalisation des actions.
- Horodatage des événements.
- Identification des acteurs.

### Information Disclosure (divulgation)
Risque : accès non autorisé aux incidents.

Mesures :
- Segmentation réseau.
- Contrôle des accès.
- Chiffrement des communications.

### Denial of Service (déni de service)
Risque : saturation de l'API.

Mesures :
- Limitation du nombre de requêtes.
- Surveillance des ressources.
- Filtrage réseau.

### Elevation of Privilege (élévation de privilèges)
Risque : un agent obtient des droits administrateur.

Mesures :
- Séparation des rôles.
- Vérification des autorisations.
- Principe du moindre privilège.

## 4. Politique de filtrage

Les pare-feu doivent appliquer une politique
de refus par défaut.

Seuls les flux documentés et nécessaires
au fonctionnement de Queen Bee sont autorisés.

Les accès administratifs doivent être limités
aux personnes et aux équipements autorisés.

## 5. Limites

Cette matrice décrit une architecture cible.

La séparation entre l'API et le service applicatif,
ainsi que le port TCP 8443, nécessiteraient un
déploiement adapté.

SQLite est utilisé localement et ne nécessite
pas l'ouverture d'un port réseau SQL.
