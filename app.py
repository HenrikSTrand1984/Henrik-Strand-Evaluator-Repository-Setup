import streamlit as st
import pandas as pd
import sys
import os

# Legg til src/ i sys.path for import
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from evaluator import calc_rammeavtale_score, calc_prosjekt_score, calc_total_score

def beregn_poeng(tilbydere, vekt_pris, vekt_miljo, vekt_kvalitet):
    """
    Beregner poeng med dynamiske vekter, ved bruk av evaluator-funksjoner.
    """
    # Valider vekter
    if vekt_pris + vekt_miljo + vekt_kvalitet != 100:
        st.error("Vekttallene må summere til 100%!")
        return pd.DataFrame()
    
    # Skaler undervekter (i desimalform for multiplikasjon)
    vekt_pris_ramme = (30 / 55) * (vekt_pris / 100)
    vekt_pris_prosjekt = (25 / 55) * (vekt_pris / 100)
    vekt_miljo_del1 = (20 / 30) * (vekt_miljo / 100)
    vekt_miljo_del2 = (10 / 30) * (vekt_miljo / 100)
    vekt_kval_komp = (5 / 15) * (vekt_kvalitet / 100)
    vekt_kval_kval = (5 / 15) * (vekt_kvalitet / 100)
    vekt_kval_gj = (5 / 15) * (vekt_kvalitet / 100)
    
    # Finn laveste priser
    laveste_pris_ramme = min(t['pris_ramme'] for t in tilbydere) if tilbydere else 1
    laveste_pris_prosjekt = min(t['pris_prosjekt'] for t in tilbydere) if tilbydere else 1
    
    resultater = []
    
    for tilbyder in tilbydere:
        p_pr = max(100 * (1 - (tilbyder['pris_ramme'] / laveste_pris_ramme - 1)), 0) if laveste_pris_ramme > 0 else 0
        p_pp = max(100 * (1 - (tilbyder['pris_prosjekt'] / laveste_pris_prosjekt - 1)), 0) if laveste_pris_prosjekt > 0 else 0
        p_km2 = sum(tilbyder['koyretøy_poeng']) / 4 if len(tilbyder['koyretøy_poeng']) == 4 else 0
        p_km1 = tilbyder['p_km1']
        p_ko = tilbyder['p_ko']
        p_kv = tilbyder['p_kv']
        p_gj = tilbyder['p_gj']
        
        # Bruk evaluator med konfigurerbare vekter
        r_score = calc_rammeavtale_score(
            p_pr, p_km1, p_km2, p_ko, p_kv, p_gj,
            vekt_pris_ramme=vekt_pris_ramme,
            vekt_miljo_del1=vekt_miljo_del1,
            vekt_miljo_del2=vekt_miljo_del2,
            vekt_kompetanse=vekt_kval_komp,
            vekt_kvalitet=vekt_kval_kval,
            vekt_gjennomforing=vekt_kval_gj
        )
        p_score = calc_prosjekt_score(p_pp, vekt_pris_prosjekt=vekt_pris_prosjekt)
        total = calc_total_score(
            p_pr, p_km1, p_km2, p_ko, p_kv, p_gj, p_pp,
            vekt_pris_ramme=vekt_pris_ramme,
            vekt_miljo_del1=vekt_miljo_del1,
            vekt_miljo_del2=vekt_miljo_del2,
            vekt_kompetanse=vekt_kval_komp,
            vekt_kvalitet=vekt_kval_kval,
            vekt_gjennomforing=vekt_kval_gj,
            vekt_pris_prosjekt=vekt_pris_prosjekt
        )
        
        resultater.append({
            'navn': tilbyder['navn'],
            'p_pr': round(p_pr, 2),
            'p_pp': round(p_pp, 2),
            'p_km1': p_km1,
            'p_km2': p_km2,
            'p_ko': p_ko,
            'p_kv': p_kv,
            'p_gj': p_gj,
            'r_score': round(r_score, 2),
            'p_score': round(p_score, 2),
            'total_poeng': total
        })
    
    resultater.sort(key=lambda x: x['total_poeng'], reverse=True)
    return pd.DataFrame(resultater)

# Resten av Streamlit-koden er lik tidligere, men med hjelpetekst
st.title("Ventilasjonskalkulator - Simuler Prisstrategier")

st.header("Justér vekttall for kategorier (må summere til 100%)")
with st.expander("Hjelp: Vekttall"):
    st.write("Endre disse for å simulere ulike anbudsstrategier. Default: Pris 55%, Miljø 30%, Kvalitet 15%.")
col1, col2, col3 = st.columns(3)
vekt_pris = col1.slider("Pris-vekt (%)", 0, 100, 55)
vekt_miljo = col2.slider("Klima/Miljø-vekt (%)", 0, 100, 30)
vekt_kvalitet = col3.slider("Kvalitet-vekt (%)", 0, 100, 15)

# Input-seksjon (lik tidligere, med validering)
st.header("Legg inn data for tilbydere")
if 'tilbydere' not in st.session_state:
    st.session_state.tilbydere = []

num_tilbydere = st.number_input("Antall tilbydere å legge inn", min_value=1, max_value=10, value=1)

for i in range(num_tilbydere):
    with st.expander(f"Tilbyder {i+1}"):
        navn = st.text_input(f"Navn for tilbyder {i+1}", value=f"Tilbyder {i+1}")
        pris_ramme = st.number_input(f"Pris rammeavtale for {navn}", min_value=0.0, value=500000.0)
        pris_prosjekt = st.number_input(f"Pris prosjekt for {navn}", min_value=0.0, value=300000.0)
        p_km1 = st.slider(f"P_km1 (Miljø del 1) for {navn}", 0, 100, 80)
        p_ko = st.slider(f"P_ko (Kompetanse) for {navn}", 0, 100, 90)
        p_kv = st.slider(f"P_kv (Kvalitet) for {navn}", 0, 100, 85)
        p_gj = st.slider(f"P_gj (Gjennomføring) for {navn}", 0, 100, 92)
        
        st.subheader("Kjøretøy-poeng (4 stk, 0-100)")
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        k1 = col_k1.number_input("K1", min_value=0, max_value=100, value=100)
        k2 = col_k2.number_input("K2", min_value=0, max_value=100, value=80)
        k3 = col_k3.number_input("K3", min_value=0, max_value=100, value=60)
        k4 = col_k4.number_input("K4", min_value=0, max_value=100, value=90)
        koyretøy_poeng = [k1, k2, k3, k4]
        
        if st.button(f"Lagre tilbyder {i+1}"):
            if pris_ramme <= 0 or pris_prosjekt <= 0:
                st.error("Priser må være positive!")
            else:
                st.session_state.tilbydere.append({
                    'navn': navn,
                    'pris_ramme': pris_ramme,
                    'pris_prosjekt': pris_prosjekt,
                    'koyretøy_poeng': koyretøy_poeng,
                    'p_km1': p_km1,
                    'p_ko': p_ko,
                    'p_kv': p_kv,
                    'p_gj': p_gj
                })
                st.success(f"{navn} lagret!")

# Beregn-knapp
if st.button("Beregn poeng og ranger (simuler strategi)"):
    if st.session_state.tilbydere:
        resultater_df = beregn_poeng(st.session_state.tilbydere, vekt_pris, vekt_miljo, vekt_kvalitet)
        if not resultater_df.empty:
            st.header("Beregnet resultater (rangert)")
            st.dataframe(resultater_df)
            
            csv = resultater_df.to_csv(index=False).encode('utf-8')
            st.download_button("Last ned som CSV", csv, "resultater.csv", "text/csv")
            
            txt_content = "Rangert etter total poeng:\n"
            for _, row in resultater_df.iterrows():
                txt_content += f"{row['navn']}:\n"
                for col in resultater_df.columns[1:]:
                    txt_content += f"  {col}: {row[col]}\n"
                txt_content += "\n"
            st.download_button("Last ned som TXT", txt_content, "resultater.txt", "text/plain")
    else:
        st.warning("Legg inn minst én tilbyder først!")

if st.button("Tilbakestill data"):
    st.session_state.tilbydere = []
    st.success("Data tilbakestilt!")
