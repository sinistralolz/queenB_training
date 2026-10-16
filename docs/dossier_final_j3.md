
# Queen Bee - Dossier final de livraison J3

## 1. Présentation du projet

Queen Bee est une application de cybersécurité
destinée à recevoir et analyser des événements
de sécurité, puis à gérer les incidents détectés.

Le projet repose sur une architecture hexagonale
séparant le domaine métier, les services applicatifs
et les adaptateurs techniques.

## 2. Modèle de menaces

Le modèle de menaces identifie les actifs sensibles,
les acteurs, les risques et les mesures de protection.

Document associé :
- docs/threat_model.md

Les risques sont étudiés selon la méthode STRIDE.

## 3. Sécurisation du code

Sept catégories de vulnérabilités ont été traitées :

1. Secret codé en dur.
2. Expression régulière vulnérable au ReDoS.
3. Désérialisation dangereuse avec Pickle.
4. Injection SQL.
5. Contrôle d'autorisation insuffisant.
6. Authentification interservices insuffisante.
7. Comparaison non sécurisée des jetons.

Des tests de non-régression ont été ajoutés.

Les tests historiques de démonstration des
vulnérabilités ont été conservés séparément.

## 4. Qualité et tests

Dernier résultat observé :

- Ruff : validé.
- mypy : validé.
- pytest : 102 tests réussis.
- Couverture du code : 90,37 %.
- Bandit : aucune alerte bloquante.
- Architecture : 1 contrat respecté, 0 rompu.

Commande utilisée :

    make check

Les tests historiques du laboratoire vulnérable
sont exclus de cette validation.

L'audit réel des dépendances reste à finaliser.

## 5. Décisions d'architecture

Les choix techniques sont documentés
dans les ADR du dossier :

- docs/adr/

Ils couvrent notamment l'architecture
hexagonale, les corrections de sécurité
et la protection de l'infrastructure.

## 6. Infrastructure sécurisée

L'architecture cible comprend :

- Une zone Agents.
- Une DMZ pour l'API.
- Une zone applicative.
- Une zone de données protégée.
- Une zone de supervision.

Documents associés :

- docs/infrastructure/zones_reseau.md
- docs/infrastructure/matrice_flux.md
- docs/infrastructure/secrets_journalisation.md
- docs/infrastructure/sauvegardes_pra.md
- docs/uml/infrastructure_j3.puml

La segmentation et les services de supervision
sont proposés, mais non déployés.

## 7. Diagrammes d'architecture

Les diagrammes UML et C4 présentent
les composants et leurs interactions.

Documents existants :

- docs/uml/c4_contexte.puml
- docs/uml/patterns_j2.puml
- docs/uml/infrastructure_j3.puml

Le diagramme C4 de niveau 2 reste à vérifier
ou à compléter.

## 8. Recette et décision Go / No-Go

La décision de livraison doit prendre en compte :

- La réussite des tests automatisés.
- Le respect du seuil de couverture.
- Les contrôles de sécurité.
- La validation de l'architecture.
- La documentation des risques résiduels.
- La vérification des dépendances.

Statut actuel : validation finale en cours.

## 9. Traçabilité et livraison

Les modifications sont versionnées avec Git.

Le tag de livraison attendu est :

    j3-rendu

Le tag sera créé après les dernières vérifications
et la validation du dossier final.
