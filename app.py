import streamlit as st
import pandas as pd
import plotly.express as px

# Configurare titlu paginii
st.set_page_config(page_title="Analiză Prețuri Imobiliare", layout="wide")

st.title("🏠 Analiză Prețuri Imobiliare")
st.write("Această aplicație analizează datele din fișierul `housing.csv`.")

# Încărcarea datelor
@st.cache_data
def load_data():
    try:
        # Se presupun coloanele: 'Neighborhood', 'Area', 'Price'
        df = pd.read_csv('housing.csv')
        return df
    except FileNotFoundError:
        st.error("Eroare: Fișierul 'housing.csv' nu a fost găsit. Te rugăm să îl adaugi în folderul aplicației.")
        return None

df = load_data()

if df is not None:
    # Afișarea primelor rânduri pentru verificare
    with st.expander("Vezi datele brute"):
        st.write(df.head())

    # Crearea layout-ului cu două coloane pentru grafice
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Preț vs. Suprafață")
        # Scatter Plot
        fig_scatter = px.scatter(
            df,
            x="Area",
            y="Price",
            color="Neighborhood",
            hover_name="Neighborhood",
            title="Relația dintre Suprafață și Preț",
            labels={"Area": "Suprafață (mp)", "Price": "Preț (EUR)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("Preț Mediu pe Cartier")
        # Agregăm datele pentru Bar Chart
        df_avg = df.groupby('Neighborhood')['Price'].mean().reset_index()

        # Bar Chart
        fig_bar = px.bar(
            df_avg,
            x="Neighborhood",
            y="Price",
            title="Preț Mediu pe Cartier",
            labels={"Neighborhood": "Cartier", "Price": "Preț Mediu (EUR)"},
            color="Price",
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("Așteptăm încă încărcarea datelor...")