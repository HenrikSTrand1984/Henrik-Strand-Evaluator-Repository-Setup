
---

## src/evaluator.py
```python
"""
Evalueringsfunksjoner for tildelingskriterier.
"""

def calc_rammeavtale_score(
    pris_ramme: float,
    klima_miljo_del1: float,
    klima_miljo_del2: float,
    kompetanse: float,
    kvalitet: float,
    gjennomforing: float
) -> float:
    """
    Beregn rammeavtale-score (maks 75).
    Vekter: 30% pris, 20% miljø del1, 10% miljø del2,
            5% kompetanse, 5% kvalitet, 5% gjennomføring.
    """
    return (
        pris_ramme * 0.30 +
        klima_miljo_del1 * 0.20 +
        klima_miljo_del2 * 0.10 +
        kompetanse * 0.05 +
        kvalitet * 0.05 +
        gjennomforing * 0.05
    )


def calc_prosjekt_score(pris_prosjekt: float) -> float:
    """
    Beregn prosjekt-score (maks 25).
    Vekt: 25% pris prosjekt.
    """
    return pris_prosjekt * 0.25


def calc_total_score(
    pris_ramme: float,
    klima_miljo_del1: float,
    klima_miljo_del2: float,
    kompetanse: float,
    kvalitet: float,
    gjennomforing: float,
    pris_prosjekt: float
) -> float:
    """
    Total score 0–100 = rammeavtale + prosjekt.
    """
    r_score = calc_rammeavtale_score(
        pris_ramme, klima_miljo_del1, klima_miljo_del2,
        kompetanse, kvalitet, gjennomforing
    )
    p_score = calc_prosjekt_score(pris_prosjekt)
    return round(r_score + p_score, 2)
