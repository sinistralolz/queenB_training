
# ADR-0003 : Protection contre les attaques ReDoS

**Statut :** Accepté

**Contexte :** L'expression régulière de validation des noms contenait des quantificateurs imbriqués, entraînant un risque de déni de service par consommation excessive du processeur.

**Décision :** Remplacer l'expression vulnérable par une expression sans quantificateurs imbriqués, avec un format de nom strict.

**Conséquences :** Les noms invalides sont rejetés rapidement. Certains formats auparavant acceptés, notamment les espaces en début ou fin de nom, ne sont plus autorisés.

**Vérification :** `tests/test_lab_redos.py` valide les noms autorisés, le rejet des noms invalides et le traitement rapide d'une entrée longue.
