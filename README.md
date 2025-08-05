# Ventilasjonskalkulator

En Python-app for å beregne poeng i ventilasjonsanbud basert på pris, miljø og kvalitet. Inkluderer en interaktiv Streamlit-app for simulering av prisstrategier.

## Installasjon
1. Klon repo: `git clone https://github.com/ditt-brukernavn/ventilasjons-kalkulator.git`
2. Installer avhengigheter: `pip install -r requirements.txt`
3. Kjør app: `streamlit run app.py`

## Struktur
- `src/evaluator.py`: Kjerneberegningsfunksjoner.
- `tests/test_evaluator.py`: Tester med pytest.
- `app.py`: Streamlit-grensesnitt for input og simulering.

## Kjøring av tester
`pytest tests/`

## Lisens
MIT License
