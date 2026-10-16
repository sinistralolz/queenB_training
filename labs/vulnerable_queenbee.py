
# ruff: noqa
"""Variante de laboratoire Queen Bee — J3-A1.

Failles 1 à 6 corrigées.
Faille 7 encore présente.
"""

import hmac
import json
import os
import re
import sqlite3


# FAILLE-1 CORRIGÉE : secret depuis l'environnement.
def get_api_key() -> str:
    key = os.environ.get("QUEENBEE_LAB_API_KEY")

    if not key:
        raise RuntimeError("QUEENBEE_LAB_API_KEY non configurée")

    return key


# FAILLE-2 CORRIGÉE : protection ReDoS.
USER_RE = re.compile(r"^[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)*$")


conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE incident (id INTEGER PRIMARY KEY, ip TEXT, status TEXT)"
)


# FAILLE-3 CORRIGÉE : JSON au lieu de pickle.
def receive_agent_message(raw: bytes) -> dict:
    message = json.loads(raw)

    if not isinstance(message, dict):
        raise ValueError("Le message doit être un objet JSON")

    return message


def is_valid_username(name: str) -> bool:
    return USER_RE.fullmatch(name) is not None


# FAILLE-4 CORRIGÉE : requête SQL paramétrée.
def find_incidents(ip: str):
    return conn.execute(
        "SELECT * FROM incident WHERE ip = ?",
        (ip,),
    ).fetchall()


# FAILLE-5 CORRIGÉE : contrôle des autorisations.
# Simulation locale des rôles.
USER_ROLES = {
    "administrateur": "admin",
    "analyste": "analyst",
    "intrus": "viewer",
}


def close_incident(user: str, incident_id: int) -> None:
    role = USER_ROLES.get(user)

    if role not in {"admin", "analyst"}:
        raise PermissionError(
            "Utilisateur non autorisé à fermer cet incident"
        )

    conn.execute(
        "UPDATE incident SET status='closed' WHERE id=?",
        (incident_id,),
    )


# FAILLE-6 CORRIGÉE : authentification inter-services.
def get_service_token() -> str:
    """Charge un secret distinct de la clé API des agents."""
    token = os.environ.get("QUEENBEE_SERVICE_TOKEN")

    if not token:
        raise RuntimeError("QUEENBEE_SERVICE_TOKEN non configuré")

    return token


def call_enrichment_service(ip: str, token: str) -> dict:
    """Refuse les appels sans jeton inter-services valide."""
    if not hmac.compare_digest(token, get_service_token()):
        raise PermissionError("Service non authentifié")

    return {"ip": ip, "reputation": "unknown"}


# FAILLE-7 : comparaison non constante.
def check_token(token: str) -> bool:
    return token == get_api_key()
