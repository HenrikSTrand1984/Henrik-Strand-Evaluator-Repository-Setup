import pytest
from src.evaluator import calc_rammeavtale_score, calc_prosjekt_score, calc_total_score


def test_rammeavtale():
    assert round(calc_rammeavtale_score(91, 90, 82.5, 95, 90, 85), 2) == 67.05


def test_prosjekt():
    assert calc_prosjekt_score(88) == 22.0


def test_total():
    total = calc_total_score(91, 90, 82.5, 95, 90, 85, 88)
    assert total == 89.05
