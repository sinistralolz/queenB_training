
# A2 - Analyse du script hérité LogWatcher

## Problèmes SOLID et de sécurité

| Élément du code | Problème | Conséquence | Correction |
|---|---|---|---|
| Classe LogWatcher | Violation SRP : une seule classe gère plusieurs responsabilités | Code difficile à maintenir et tester | Séparer les objets métier, la détection, le stockage et les alertes |
| SMTP_PASSWORD | Mot de passe écrit directement dans le code | Risque de divulgation du secret | Lire le secret depuis une variable d'environnement |
| DB.execute | Requête SQL construite avec une f-string | Risque d'injection SQL | Utiliser une requête SQL paramétrée |
| open(self.path) | Fichier ouvert sans fermeture explicite | Risque de fuite de ressources | Utiliser `with open(...)` |
| re.search | Expression régulière trop permissive | Analyse incorrecte de certaines lignes | Utiliser une regex ancrée et valider les données |
| alert() | Dépendance directe à SMTP | Tests difficiles sans serveur mail | Définir une interface avec `Protocol` |
| report() | Violation OCP : ajout d'un format = modification de la méthode | Difficulté à étendre le programme | Séparer les stratégies d'export |
| report("html") | Contenu non échappé | Risque de XSS si le rapport est affiché dans un navigateur | Échapper les caractères HTML |
| DB et SMTP | Dépendances techniques directement liées à la logique métier | Couplage fort et faible testabilité | Isoler les adaptateurs techniques |
```
