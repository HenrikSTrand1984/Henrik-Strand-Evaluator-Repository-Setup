import pytest
from src.evaluator import calc_rammeavtale_score, calc_prosjekt_score, calc_total_score

def test_rammeavtale():
    assert calc_rammeavtale_score(91, 90, 82.5, 95, 90, 85) == 67.05

def test_prosjekt():
    assert calc_prosjekt_score(88) == 22.0

def test_total():
    assert calc_total_score(91, 90, 82.5, 95, 90, 85, 88) == 89.05

def test_rammeavtale_edge_cases():
    assert calc_rammeavtale_score(0, 0, 0, 0, 0, 0) == 0.0
    assert calc_rammeavtale_score(100, 100, 100, 100, 100, 100) == 75.0
    with pytest.raises(ValueError):
        calc_rammeavtale_score(101, 100, 100, 100, 100, 100)

def test_prosjekt_edge_cases():
    assert calc_prosjekt_score(0) == 0.0
    assert calc_prosjekt_score(100) == 25.0
    with pytest.raises(ValueError):
        calc_prosjekt_score(-1)

def test_total_edge_cases():
    assert calc_total_score(0, 0, 0, 0, 0, 0, 0) == 0.0
    assert calc_total_score(100, 100, 100, 100, 100, 100, 100) == 100.0
    with pytest.raises(ValueError):
        calc_total_score(100, 100, 100, 100, 100, 100, 101)

@pytest.mark.parametrize("vekt_pris_ramme, expected", [(0.4, 40.0), (0.3, 30.0)])
def test_konfigurerbare_vekter(vekt_pris_ramme, expected):
    assert calc_rammeavtale_score(100, 0, 0, 0, 0, 0, vekt_pris_ramme=vekt_pris_ramme) == expected
