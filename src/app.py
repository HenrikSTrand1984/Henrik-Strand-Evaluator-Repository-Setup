import streamlit as st
import pandas as pd

def beregn_poeng(df):
    """
    Beregner poeng basert på DataFrame-input.
    """
    tilbydere = df.to_dict(orient='records')
    
    # Finn laveste priser
    laveste_pris_ramme = min(t['pris_ramme'] for t in tilbydere)
    laveste_pris_prosjekt = min(t['pris_prosjekt'] for t in tilbydere)
    
    resultater = []
    
    for tilbyder in tilbydere:
        p_pr = max(100 * (1 - (tilbyder['pris_ramme'] / laveste_pris_ramme - 1)), 0) if laveste_pris_ramme > 0 else 0
        p_pp = max(100 * (1 - (tilbyder['pris_prosjekt'] / laveste_pris_prosjekt - 1)), 0) if laveste_pris_prosjekt > 0 else 0
        
        # Kjøretøy-poeng som gjennomsnitt (antatt list i CSV som streng, f.eks. "[100,90,80,100]")
        koyretøy_poeng = eval(tilbyder['koyretøy_poeng'])  # Vær forsiktig med eval i prod!
        p_km2 = sum(koyretøy_poeng) / 4 if len(koyretøy_poeng) == 4 else 0
        
        p_km1 = tilbyder['p_km1']
        p_ko = tilbyder['p_ko']
        p_kv = tilbyder['p_kv']
        p_gj = tilbyder['p_gj']
        
        r_score = (p_pr * 0.3) + (p_km1 * 0.2) + (p_km2 * 0.1) + (p_ko * 0.05) + (p_kv * 0.05) + (p_gj * 0.05)
        p_score = p_pp * 0.25
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
st.title("Ventilasjonskalkulator")

uploaded_file = st.file_uploader("Last opp CSV med tilbyder-data", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Innlastet data:")
    st.dataframe(df)
    
    resultater_df = beregn_poeng(df)
    st.write("Beregnet resultater (rangert):")
    st.dataframe(resultater_df)
    
    # Eksport-knapp
    csv = resultater_df.to_csv(index=False).encode('utf-8')
    st.download_button("Last ned resultater som CSV", csv, "resultater.csv", "text/csv")

# Eksempel-CSV-mal
st.write("Eksempel-CSV-format (kopier til fil):")
st.code("""navn,pris_ramme,pris_prosjekt,koyretøy_poeng,p_km1,p_ko,p_kv,p_gj
GK,450000,290000,[100,90,80,100],98,95,95,95
Tilbyder B,500000,320000,[80,60,40,80],80,85,90,88
Tilbyder C,550000,280000,[100,100,100,100],70,95,80,85""")
