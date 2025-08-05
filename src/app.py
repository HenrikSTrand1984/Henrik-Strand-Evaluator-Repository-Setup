import streamlit as st
import pandas as pd

def beregn_poeng(tilbydere, vekt_pris, vekt_miljo, vekt_kvalitet):
    """
    Beregner poeng med dynamiske vekter.
    Undervekter skalerer proporsjonalt til hovedvekter.
    """
    # Valider at vekter summerer til 100%
    if vekt_pris + vekt_miljo + vekt_kvalitet != 100:
        st.error("Vekttallene må summere til 100%!")
        return pd.DataFrame()
    
    # Skaler undervekter (i prosent, så del på 100 for multiplikasjon)
    vekt_pris_ramme = (30 / 55) * (vekt_pris / 100)
    vekt_pris_prosjekt = (25 / 55) * (vekt_pris / 100)
    vekt_miljo_del1 = (20 / 30) * (vekt_miljo / 100)
    vekt_miljo_del2 = (10 / 30) * (vekt_miljo / 100)
    vekt_kval_komp = (5 / 15) * (vekt_kvalitet / 100)
    vekt_kval_kval = (5 / 15) * (vekt_kvalitet / 100)
    vekt_kval_gj = (5 / 15) * (vekt_kvalitet / 100)
    
    # Finn laveste priser for relativ beregning
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
        
        # Beregn med skalerte vekter
        r_score = (p_pr * vekt_pris_ramme) + (p_km1 * vekt_miljo_del1) + (p_km2 * vekt_miljo_del2) + \
                  (p_ko * vekt_kval_komp) + (p_kv * vekt_kval_kval) + (p_gj * vekt_kval_gj)
        p_score = p_pp * vekt_pris_prosjekt
        e_p = r_score + p_score
        
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
            'total_poeng': round(e_p, 2)
        })
    
    resultater.sort(key=lambda x: x['total_poeng'], reverse=True)
    return pd.DataFrame(resultater)

# Streamlit-app
st.title("Ventilasjonskalkulator - Simuler Prisstrategier")

# Seksjon for vekter (sliders for simulering)
st.header("Justér vekttall for kategorier (må summere til 100%)")
col1, col2, col3 = st.columns(3)
vekt_pris = col1.slider("Pris-vekt (%)", 0, 100, 55)
vekt_miljo = col2.slider("Klima/Miljø-vekt (%)", 0, 100, 30)
vekt_kvalitet = col3.slider("Kvalitet-vekt (%)", 0, 100, 15)

# Seksjon for tilbyder-input
st.header("Legg inn data for tilbydere")
if 'tilbydere' not in st.session_state:
    st.session_state.tilbydere = []

num_tilbydere = st.number_input("Antall tilbydere å legge inn", min_value=1, max_value=10, value=1)

for i in range(num_tilbydere):
    with st.expander(f"Tilbyder {i+1}"):
        navn = st.text_input(f"Navn for tilbyder {i+1}", value=f"Tilbyder {i+1}")
        pris_ramme = st.number_input(f"Pris rammeavtale for {navn}", value=500000.0)
        pris_prosjekt = st.number_input(f"Pris prosjekt for {navn}", value=300000.0)
        p_km1 = st.slider(f"P_km1 (Miljø del 1) for {navn}", 0, 100, 80)
        p_ko = st.slider(f"P_ko (Kompetanse) for {navn}", 0, 100, 90)
        p_kv = st.slider(f"P_kv (Kvalitet) for {navn}", 0, 100, 85)
        p_gj = st.slider(f"P_gj (Gjennomføring) for {navn}", 0, 100, 92)
        
        # Kjøretøy-poeng som 4 separate inputs
        st.subheader("Kjøretøy-poeng (4 stk, 0-100)")
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        k1 = col_k1.number_input("K1", 0, 100, 100)
        k2 = col_k2.number_input("K2", 0, 100, 80)
        k3 = col_k3.number_input("K3", 0, 100, 60)
        k4 = col_k4.number_input("K4", 0, 100, 90)
        koyretøy_poeng = [k1, k2, k3, k4]
        
        # Lagre tilbyder midlertidig
        temp_tilbyder = {
            'navn': navn,
            'pris_ramme': pris_ramme,
            'pris_prosjekt': pris_prosjekt,
            'koyretøy_poeng': koyretøy_poeng,
            'p_km1': p_km1,
            'p_ko': p_ko,
            'p_kv': p_kv,
            'p_gj': p_gj
        }
        
        if st.button(f"Lagre tilbyder {i+1}"):
            st.session_state.tilbydere.append(temp_tilbyder)
            st.success(f"{navn} lagret!")

# Beregn og vis resultater
if st.button("Beregn poeng og ranger (simuler strategi)"):
    if st.session_state.tilbydere:
        resultater_df = beregn_poeng(st.session_state.tilbydere, vekt_pris, vekt_miljo, vekt_kvalitet)
        if not resultater_df.empty:
            st.header("Beregnet resultater (rangert)")
            st.dataframe(resultater_df)
            
            # Eksport
            csv = resultater_df.to_csv(index=False).encode('utf-8')
            st.download_button("Last ned resultater som CSV", csv, "resultater.csv", "text/csv")
            
            txt_content = "Rangert etter total poeng:\n"
            for _, row in resultater_df.iterrows():
                txt_content += f"{row['navn']}:\n"
                for col in resultater_df.columns[1:]:
                    txt_content += f"  {col}: {row[col]}\n"
                txt_content += "\n"
            st.download_button("Last ned resultater som TXT", txt_content, "resultater.txt", "text/plain")
    else:
        st.warning("Legg inn minst én tilbyder først!")

# Tilbakestill-knapp
if st.button("Tilbakestill alle data"):
    st.session_state.tilbydere = []
    st.success("Data tilbakestilt!")
