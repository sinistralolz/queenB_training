
# ruff: noqa
"""Variante de laboratoire Queen Bee — J3-A1.

Les 7 failles de sécurité ont été corrigées.
Version utilisée pour les tests de non-régression.
"""

import hmac
import json
import os
import re
import sqlite3


# FAILLE-1 CORRIGÉE : secret depuis l'environnement.
def get_api_key() -> str:
    """Récupère la clé API depuis une variable d'environnement."""
    key = os.environ.get("QUEENBEE_LAB_API_KEY")

    if not key:
        raise RuntimeError("QUEENBEE_LAB_API_KEY non configurée")

    return key


# FAILLE-2 CORRIGÉE : protection contre les ReDoS.
USER_RE = re.compile(r"^[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)*$")


conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE incident (id INTEGER PRIMARY KEY, ip TEXT, status TEXT)"
)


# FAILLE-3 CORRIGÉE : JSON au lieu de pickle.
def receive_agent_message(raw: bytes) -> dict:
    """Décode un message JSON sans exécuter de code."""
    message = json.loads(raw)

    if not isinstance(message, dict):
        raise ValueError("Le message doit être un objet JSON")

    return message


def is_valid_username(name: str) -> bool:
    """Vérifie le format du nom d'utilisateur."""
    return USER_RE.fullmatch(name) is not None


# FAILLE-4 CORRIGÉE : requête SQL paramétrée.
def find_incidents(ip: str):
    """Recherche les incidents sans injection SQL."""
    return conn.execute(
        "SELECT * FROM incident WHERE ip = ?",
        (ip,),
    ).fetchall()


# FAILLE-5 CORRIGÉE : contrôle des autorisations.
# Simulation locale des rôles pour le laboratoire.
USER_ROLES = {
    "administrateur": "admin",
    "analyste": "analyst",
    "intrus": "viewer",
}


def close_incident(user: str, incident_id: int) -> None:
    """Autorise uniquement les administrateurs et analystes."""
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


# FAILLE-7 CORRIGÉE : comparaison sécurisée des jetons.
def check_token(token: str) -> bool:
    """Compare les jetons avec une fonction adaptée aux secrets."""
    return hmac.compare_digest(token, get_api_key())

