# Ventilasjonskalkulator

En Python-app for å beregne poeng i ventilasjonsanbud basert på pris, miljø og kvalitet. Inkluderer en interaktiv Streamlit-app for simulering av prisstrategier.

## Installasjon
1. Klon repo: `git clone https://github.com/ditt-brukernavn/ventilasjons-kalkulator.git`
2. Opprett virtuelt miljø: `python -m venv .venv` og aktiver det.
3. Installer avhengigheter: `pip install -r requirements.txt`
4. Kjør app: `streamlit run app.py`

## Struktur
- `src/evaluator.py`: Kjerneberegningsfunksjoner med konfigurerbare vekter.
- `tests/test_evaluator.py`: Tester med pytest, inkludert edge-cases.
- `app.py`: Streamlit-grensesnitt for input, vektsimulering og resultatvisning.
- `.env.example`: Eksempel for miljøvariabler (kopier til .env hvis nødvendig).

## Kjøring av tester
`pytest tests/`

## Lisens
MIT License (se LICENSE for detaljer)
