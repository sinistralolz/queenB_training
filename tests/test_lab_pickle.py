
"""Tests de non-régression de la faille 3 : désérialisation."""

import json
import pickle

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_3_accepte_json() -> None:
    message = {"agent": "poste-01", "event": "login_failed"}
    raw = json.dumps(message).encode("utf-8")

    assert vuln.receive_agent_message(raw) == message


@pytest.mark.lab
def test_faille_3_refuse_pickle() -> None:
    raw = pickle.dumps({"agent": "poste-01"})

    with pytest.raises((ValueError, UnicodeDecodeError)):
        vuln.receive_agent_message(raw)


@pytest.mark.lab
def test_faille_3_refuse_json_non_objet() -> None:
    with pytest.raises(ValueError, match="objet JSON"):
        vuln.receive_agent_message(b'["agent-01"]')
