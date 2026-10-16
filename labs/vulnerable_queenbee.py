
# ruff: noqa
"""VARIANTE VOLONTAIREMENT FRAGILE de Queen Bee — usage LABORATOIRE uniquement (J3-A1).

Sept failles d'architecture à exploiter (en local), corriger, puis vérifier avec bandit/pip-audit.
Chaque faille porte un numéro FAILLE-n ; la correction de référence est dans src/queenbee.

FAILLE-1 corrigée : secret chargé depuis l'environnement.
"""

import os
import pickle
import re
import sqlite3


# FAILLE-1 CORRIGÉE : aucun secret codé en dur.
def get_api_key() -> str:
    """Récupère la clé depuis une variable d'environnement."""
    key = os.environ.get("QUEENBEE_LAB_API_KEY")

    if not key:
        raise RuntimeError("QUEENBEE_LAB_API_KEY non configurée")

    return key


# FAILLE-2 : quantificateurs imbriqués -> ReDoS
USER_RE = re.compile(r"^[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)*$")


conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE incident (id INTEGER PRIMARY KEY, ip TEXT, status TEXT)"
)


# FAILLE-3 : désérialisation non sûre (RCE)
def receive_agent_message(raw: bytes):
    return pickle.loads(raw)


def is_valid_username(name: str) -> bool:
    return USER_RE.match(name) is not None


# FAILLE-4 : injection SQL (f-string)
def find_incidents(ip: str):
    return conn.execute(
        f"SELECT * FROM incident WHERE ip = '{ip}'"
    ).fetchall()


# FAILLE-5 : aucune vérification d'autorisation dans la couche service
def close_incident(user: str, incident_id: int) -> None:
    conn.execute(
        "UPDATE incident SET status='closed' WHERE id=?",
        (incident_id,),
    )


# FAILLE-6 : appel inter-services sans authentification mutuelle
def call_enrichment_service(ip: str) -> dict:
    return {"ip": ip, "reputation": "unknown"}


# FAILLE-7 : comparaison non constante (timing)
def check_token(token: str) -> bool:
    return token == get_api_key()
