
# ruff: noqa
"""Variante de laboratoire Queen Bee — J3-A1.

Failles 1, 2, 3 et 4 corrigées.
Failles 5, 6 et 7 encore présentes pour les exercices suivants.
"""

import json
import os
import re
import sqlite3


# FAILLE-1 CORRIGÉE : secret chargé depuis l'environnement.
def get_api_key() -> str:
    """Récupère la clé API depuis une variable d'environnement."""
    key = os.environ.get("QUEENBEE_LAB_API_KEY")

    if not key:
        raise RuntimeError("QUEENBEE_LAB_API_KEY non configurée")

    return key


# FAILLE-2 CORRIGÉE : expression régulière sans quantificateurs imbriqués.
USER_RE = re.compile(r"^[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)*$")


conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE incident (id INTEGER PRIMARY KEY, ip TEXT, status TEXT)"
)


# FAILLE-3 CORRIGÉE : utilisation de JSON à la place de pickle.
def receive_agent_message(raw: bytes) -> dict:
    """Décode un message JSON sans exécuter de code."""
    message = json.loads(raw)

    if not isinstance(message, dict):
        raise ValueError("Le message doit être un objet JSON")

    return message


def is_valid_username(name: str) -> bool:
    return USER_RE.fullmatch(name) is not None


# FAILLE-4 CORRIGÉE : requête SQL paramétrée.
def find_incidents(ip: str):
    """Recherche les incidents sans risque d'injection SQL."""
    return conn.execute(
        "SELECT * FROM incident WHERE ip = ?",
        (ip,),
    ).fetchall()


# FAILLE-5 : aucune vérification d'autorisation.
def close_incident(user: str, incident_id: int) -> None:
    conn.execute(
        "UPDATE incident SET status='closed' WHERE id=?",
        (incident_id,),
    )


# FAILLE-6 : appel inter-services sans authentification mutuelle.
def call_enrichment_service(ip: str) -> dict:
    return {"ip": ip, "reputation": "unknown"}


# FAILLE-7 : comparaison non constante (timing).
def check_token(token: str) -> bool:
    return token == get_api_key()

