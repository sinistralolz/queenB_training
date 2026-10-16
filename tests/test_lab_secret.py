
"""Tests de non-régression de la faille 1 : secret codé en dur."""

import ast
from pathlib import Path

import pytest

from labs import vulnerable_queenbee as vuln

LAB_FILE = (
    Path(__file__).resolve().parents[1]
    / "labs"
    / "vulnerable_queenbee.py"
)


@pytest.mark.lab
def test_faille_1_aucun_secret_en_dur() -> None:
    """Vérifie que la clé API n'est plus inscrite dans le code."""
    source = LAB_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    hardcoded_secrets = [
        node.value.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "API_KEY"
            for target in node.targets
        )
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    ]

    assert not hardcoded_secrets, "Une clé API est codée en dur."


@pytest.mark.lab
def test_faille_1_refuse_secret_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Refuse l'utilisation si aucune clé n'est configurée."""
    monkeypatch.delenv("QUEENBEE_LAB_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="non configurée"):
        vuln.get_api_key()


@pytest.mark.lab
def test_faille_1_lit_secret_depuis_environnement(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Récupère la clé depuis l'environnement."""
    monkeypatch.setenv("QUEENBEE_LAB_API_KEY", "cle-fictive-pour-test")

    assert vuln.get_api_key() == "cle-fictive-pour-test"
