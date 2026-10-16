
"""Tests de laboratoire : comparaison des jetons."""

import ast
import inspect

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_7_comparaison_non_securisee() -> None:
    """Prouve l'utilisation de == pour comparer le jeton."""
    source = inspect.getsource(vuln.check_token)
    tree = ast.parse(source)

    comparisons = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Compare)
        and any(isinstance(op, ast.Eq) for op in node.ops)
    ]

    assert comparisons, "La comparaison vulnérable n'est plus présente."
