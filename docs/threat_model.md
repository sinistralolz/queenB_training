# Modèle de menaces — Queen Bee (gabarit à compléter)

## 1. Actifs

| Actif | Pourquoi il compte | C / I / D / P |
|---|---|---|
| Incidents | Permettent de suivre les attaques et les actions de réponse | C, I, P |
| Clé HMAC agents | Empêche un attaquant de se faire passer pour un agent légitime | C, I |
| Règles de détection | Permettent de reconnaître les attaques informatiques | I, D |
| Journaux de sécurité | Conservent les événements et les preuves d'attaque | I, P |
| Base de données | Stocke les incidents et leur historique | C, I, D |
| Service de détection | Analyse les événements et génère les alertes | D, I |

## 2. Acteurs
Agent (machine), Analyste SOC, Admin, Attaquant externe, Agent compromis.

## 3. Frontières de confiance
TB1 Réseau agents -> API ingestion · TB2 Application -> base · TB3 Application -> pare-feu · TB4 Analyste -> UI

## 4. STRIDE par flux
| Flux | S | T | R | I | D | E | Exigence |
|---|---|---|---|---|---|---|---|
| Agent -> Ingestion | faux agent | message altéré | | | flood | | EX-01 HMAC, EX-02 taille max, EX-03 rate limit |

## 5. Exigences de sécurité (EX-nn, testables)
- EX-01 Tout message d'agent est authentifié (HMAC-SHA256, comparaison temps constant). Test : `test_abuse_forged_signature_rejected`.
