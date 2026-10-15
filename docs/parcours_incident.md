# Queen Bee — Parcours d'un incident de sécurité

## Objectif

Décrire le parcours d'une attaque informatique, depuis sa détection par un agent jusqu'à la clôture de l'incident par un analyste SOC.

Ce parcours présente les composants utilisés, les frontières de confiance et les menaces STRIDE à prendre en compte.

## Parcours utilisateur en 7 étapes

| Étape | Action | Composant | Frontière de confiance | Menace STRIDE |
|---|---|---|---|---|
| 1 | Un agent collecte un événement suspect, par exemple plusieurs échecs de connexion SSH. | Agent de collecte | Machine surveillée vers agent | Tampering : falsification des journaux |
| 2 | L'agent transmet l'événement. Queen Bee vérifie la signature HMAC et valide le format du message. | Adaptateur entrant `agent_api` | **Frontière 1 : agent externe vers Queen Bee** | Spoofing : usurpation d'un agent |
| 3 | Le moteur analyse l'événement et applique les règles de détection. | `DetectionService` et `RuleSet` | Adaptateur entrant vers logique applicative | Tampering : événement malformé ou manipulé |
| 4 | Une alerte provoque la création d'un incident, qui est enregistré dans le dépôt. | `DetectionService` et `IncidentRepository` | **Frontière 2 : application vers stockage** | Tampering : modification des incidents |
| 5 | Queen Bee transmet une notification aux abonnés autorisés,
