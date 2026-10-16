
# ADR-0005 : Protection contre les injections SQL

**Statut :** Accepté

**Contexte :** La recherche d'incidents utilisait une f-string pour construire une requête SQL, permettant à une entrée malveillante de modifier la requête.

**Décision :** Utiliser des requêtes SQL paramétrées avec des espaces réservés (?) et transmettre les valeurs séparément.

**Conséquences :** Les entrées utilisateur sont traitées comme des données et ne peuvent plus modifier la structure de cette requête SQL.

**Vérification :** Les deux tests de tests/test_lab_sql.py passent, notamment celui qui vérifie le blocage de l'injection SQL.
