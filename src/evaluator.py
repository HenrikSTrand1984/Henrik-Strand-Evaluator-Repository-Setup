"""
Evalueringsfunksjoner for tildelingskriterier.
"""
from typing import float

def calc_rammeavtale_score(
    pris_ramme: float,
    klima_miljo_del1: float,
    klima_miljo_del2: float,
    kompetanse: float,
    kvalitet: float,
    gjennomforing: float,
    vekt_pris_ramme: float = 0.30,
    vekt_miljo_del1: float = 0.20,
    vekt_miljo_del2: float = 0.10,
    vekt_kompetanse: float = 0.05,
    vekt_kvalitet: float = 0.05,
    vekt_gjennomforing: float = 0.05
) -> float:
    """
    Beregn rammeavtale-score (maks 75 med default vekter).
    Vekter: Konfigurerbare med defaults.
    
    Eksempel:
        >>> calc_rammeavtale_score(100, 100, 100, 100, 100, 100)
        75.0
    """
    if not all(0 <= val <= 100 for val in [pris_ramme, klima_miljo_del1, klima_miljo_del2, kompetanse, kvalitet, gjennomforing]):
        raise ValueError("Alle poeng må være mellom 0 og 100.")
    score = (
        pris_ramme * vekt_pris_ramme +
        klima_miljo_del1 * vekt_miljo_del1 +
        klima_miljo_del2 * vekt_miljo_del2 +
        kompetanse * vekt_kompetanse +
        kvalitet * vekt_kvalitet +
        gjennomforing * vekt_gjennomforing
    )
    return round(score, 2)

def calc_prosjekt_score(
    pris_prosjekt: float,
    vekt_pris_prosjekt: float = 0.25
) -> float:
    """
    Beregn prosjekt-score (maks 25 med default vekt).
    
    Eksempel:
        >>> calc_prosjekt_score(100)
        25.0
    """
    if not 0 <= pris_prosjekt <= 100:
        raise ValueError("Poeng må være mellom 0 og 100.")
    return round(pris_prosjekt * vekt_pris_prosjekt, 2)

def calc_total_score(
    pris_ramme: float,
    klima_miljo_del1: float,
    klima_miljo_del2: float,
    kompetanse: float,
    kvalitet: float,
    gjennomforing: float,
    pris_prosjekt: float,
    vekt_pris_ramme: float = 0.30,
    vekt_miljo_del1: float = 0.20,
    vekt_miljo_del2: float = 0.10,
    vekt_kompetanse: float = 0.05,
    vekt_kvalitet: float = 0.05,
    vekt_gjennomforing: float = 0.05,
    vekt_pris_prosjekt: float = 0.25
) -> float:
    """
    Total score 0–100 = rammeavtale + prosjekt.
    
    Eksempel:
        >>> calc_total_score(100, 100, 100, 100, 100, 100, 100)
        100.0
    """
    r_score = calc_rammeavtale_score(
        pris_ramme, klima_miljo_del1, klima_miljo_del2, kompetanse, kvalitet, gjennomforing,
        vekt_pris_ramme, vekt_miljo_del1, vekt_miljo_del2, vekt_kompetanse, vekt_kvalitet, vekt_gjennomforing
    )
    p_score = calc_prosjekt_score(pris_prosjekt, vekt_pris_prosjekt)
    return round(r_score + p_score, 2)
