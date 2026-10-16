
"""Tests de non-régression de la faille 2 : ReDoS."""

import time

import pytest

from labs import vulnerable_queenbee as vuln


@pytest.mark.lab
def test_faille_2_nom_valide() -> None:
    assert vuln.is_valid_username("Agent 007")


@pytest.mark.lab
def test_faille_2_nom_invalide() -> None:
    assert not vuln.is_valid_username("Agent!")


@pytest.mark.lab
def test_faille_2_entree_longue_rejetee() -> None:
    """Une entrée longue et invalide doit être rejetée rapidement."""
    start = time.perf_counter()
    result = vuln.is_valid_username("a" * 1000 + "!")
    duration = time.perf_counter() - start

    assert not result
    assert duration < 0.5

