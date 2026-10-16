
"""Tests de laboratoire pour la faille 1 : secret codé en dur."""

import ast
from pathlib import Path

import pytest


LAB_FILE = (
    Path(__file__).resolve().parents[1]
    / "labs"
    / "vulnerable_queenbee.py"
)


@pytest.mark.lab
def test_faille_1_secret_en_dur() -> None:
    """Démontre qu'une clé sensible est inscrite dans le code."""
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

    assert hardcoded_secrets, (
        "La vulnérabilité n'est plus présente : "
        "aucune clé API codée en dur."
    )
