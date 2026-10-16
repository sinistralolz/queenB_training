
# ADR-0004 : Désérialisation sécurisée des messages

**Statut :** Accepté

**Contexte :** Queen Bee utilisait pickle.loads() pour traiter les messages des agents, ce qui pouvait permettre l'exécution de code arbitraire.

**Décision :** Remplacer pickle par JSON et vérifier que le message reçu est un objet.

**Conséquences :** Les messages pickle sont refusés. Les agents doivent transmettre leurs événements au format JSON.

**Vérification :** Les trois tests de tests/test_lab_pickle.py passent.
