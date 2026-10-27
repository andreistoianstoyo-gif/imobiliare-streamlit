import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Data Dashboard", layout="wide")

st.title("📊 Interactive Data Dashboard")
st.write("Upload a CSV or Excel file, or explore the demo data below.")


# --- Încărcarea datelor -----------------------------------------------
@st.cache_data
def load_file(file):
    if file.name.lower().endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)  # are nevoie de openpyxl în requirements.txt


@st.cache_data
def load_demo():
    return pd.read_csv("housing.csv")


uploaded = st.file_uploader("Upload your file (CSV or Excel)", type=["csv", "xlsx"])

try:
    if uploaded is not None:
        df = load_file(uploaded)
    else:
        df = load_demo()
        st.info("Showing demo data (small real estate sample). Upload your own file to analyze it.")
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

# --- Detectăm automat tipurile de coloane ------------------------------
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

if not num_cols:
    st.error("No numeric columns found in this file, so there is nothing to chart.")
    st.stop()

with st.expander("View raw data"):
    st.dataframe(df, use_container_width=True)

# --- Filtre în bara laterală -------------------------------------------
st.sidebar.header("Filters")
filtered = df.copy()

# filtre pentru coloane text, doar dacă au puține valori (ex: cartier, categorie)
for col in cat_cols:
    options = sorted(df[col].dropna().astype(str).unique())
    if 1 < len(options) <= 20:
        chosen = st.sidebar.multiselect(col, options, default=options)
        filtered = filtered[filtered[col].astype(str).isin(chosen)]

# filtre pentru primele 3 coloane numerice
for col in num_cols[:3]:
    lo, hi = float(df[col].min()), float(df[col].max())
    if lo < hi:
        selected = st.sidebar.slider(col, lo, hi, (lo, hi))
        filtered = filtered[filtered[col].between(selected[0], selected[1])]

if filtered.empty:
    st.warning("No rows match the current filters.")
    st.stop()

# --- Numere cheie -------------------------------------------------------
st.subheader("Key numbers")
metric_col = st.selectbox("Column to summarize", num_cols)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{len(filtered):,}")
c2.metric("Average", f"{filtered[metric_col].mean():,.1f}")
c3.metric("Median", f"{filtered[metric_col].median():,.1f}")
c4.metric("Max", f"{filtered[metric_col].max():,.1f}")

# --- Grafice -------------------------------------------------------------
color_col = cat_cols[0] if cat_cols and filtered[cat_cols[0]].nunique() <= 20 else None

left, right = st.columns(2)

with left:
    st.subheader("Relationship between two columns")
    if len(num_cols) >= 2:
        x_col = st.selectbox("X axis", num_cols, index=0)
        y_col = st.selectbox("Y axis", num_cols, index=len(num_cols) - 1)
        fig_scatter = px.scatter(filtered, x=x_col, y=y_col, color=color_col)
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.write("Needs at least two numeric columns.")

with right:
    st.subheader("Average by category")
    if cat_cols:
        group_col = st.selectbox("Group by", cat_cols)
        df_avg = filtered.groupby(group_col)[metric_col].mean().reset_index()
        fig_bar = px.bar(df_avg, x=group_col, y=metric_col,
                         color=metric_col, color_continuous_scale="Viridis")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.write("No text/category columns found.")

st.subheader("Distribution")
fig_hist = px.histogram(filtered, x=metric_col, nbins=20)
st.plotly_chart(fig_hist, use_container_width=True)

# --- Descărcare date filtrate ---------------------------------------------
st.download_button(
    "Download filtered data (CSV)",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_data.csv",
    mime="text/csv",
)
