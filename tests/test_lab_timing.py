
"""Tests de non-régression : comparaison sécurisée des jetons."""

import ast
import inspect

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_7_utilise_compare_digest() -> None:
    """Vérifie que la fonction utilise hmac.compare_digest."""
    source = inspect.getsource(vuln.check_token)
    tree = ast.parse(source)

    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "compare_digest"
    ]

    assert calls, "La comparaison sécurisée n'est pas utilisée."


@pytest.mark.lab
def test_faille_7_jeton_valide(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("QUEENBEE_LAB_API_KEY", "cle-test-securisee")

    assert vuln.check_token("cle-test-securisee")


@pytest.mark.lab
def test_faille_7_jeton_invalide(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("QUEENBEE_LAB_API_KEY", "cle-test-securisee")

    assert not vuln.check_token("mauvaise-cle")
