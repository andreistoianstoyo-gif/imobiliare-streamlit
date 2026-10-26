import streamlit as st
import pandas as pd
import plotly.express as px

# Configurare titlu paginii
st.set_page_config(page_title="Real Estate Price Analysis", layout="wide")

st.title("🏠 Real Estate Price Analysis")
st.write("This application analyzes data from the housing.csv file.")

# Încărcarea datelor
@st.cache_data
def load_data():
    try:
        # Se presupun coloanele: 'Neighborhood', 'Area', 'Price'
        df = pd.read_csv('housing.csv')
        return df
    except FileNotFoundError:
        st.error("Error: The file 'housing.csv' was not found. Please add it to the application folder.")
        return None

df = load_data()

if df is not None:
    # Afișarea primelor rânduri pentru verificare
    with st.expander("View raw data"):
        st.write(df.head())

    # Crearea layout-ului cu două coloane pentru grafice
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Price vs. Surface Area")
        # Scatter Plot
        fig_scatter = px.scatter(
            df,
            x="Area",
            y="Price",
            color="Neighborhood",
            hover_name="Neighborhood",
            title="The Relationship Between Surface Area and Price",
            labels={"Area": "Surface (mp)", "Price": "Price (EUR)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("Average Price by Neighborhood")
        # Agregăm datele pentru Bar Chart
        df_avg = df.groupby('Neighborhood')['Price'].mean().reset_index()

        # Bar Chart
        fig_bar = px.bar(
            df_avg,
            x="Neighborhood",
            y="Price",
            title="Average Price by Neighborhood",
            labels={"Neighborhood": "Neighborhood", "Price": "Average Price (EUR)"},
            color="Price",
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("We are still waiting for the data to load...")