import streamlit as st
import pandas as pd

from config import (
    MAROC_INDICES,
    WORLD_INDICES
)

from market import (
    load_yahoo_data,
    load_maroc_index,
    compute_metrics,
    generate_commentary
)

st.set_page_config(
    page_title="CMR - Suivi des Indices",
    layout="wide"
)

st.title("CMR - Suivi des Indices")

# --------------------------------------------------
# MISE A JOUR MASI
# --------------------------------------------------

st.sidebar.header("Mise à jour des données")

uploaded_file = st.sidebar.file_uploader(
    "Importer un nouveau fichier MASI",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

        nouveau_df = pd.read_excel(
            uploaded_file
        )

        nouveau_df.to_excel(
            "Data_masi.xlsx",
            index=False
        )

        st.sidebar.success(
            "Fichier Data_masi.xlsx mis à jour"
        )

    except Exception as e:

        st.sidebar.error(
            f"Erreur : {e}"
        )

# --------------------------------------------------
# CHOIX DU MARCHE
# --------------------------------------------------

source = st.radio(
    "Marché",
    [
        "Maroc",
        "International"
    ]
)

try:

    if source == "Maroc":

        indice = st.selectbox(
            "Indice",
            list(MAROC_INDICES.keys())
        )

        df = load_maroc_index(
            MAROC_INDICES[indice]
        )

    else:

        indice = st.selectbox(
            "Indice",
            list(WORLD_INDICES.keys())
        )

        df = load_yahoo_data(
            WORLD_INDICES[indice]
        )

    metrics = compute_metrics(df)

    st.subheader("Indicateurs")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "1 Mois",
        f"{metrics['Performance 1 mois (%)']}%"
    )

    col2.metric(
        "3 Mois",
        f"{metrics['Performance 3 mois (%)']}%"
    )

    col3.metric(
        "YTD",
        f"{metrics['Performance YTD (%)']}%"
    )

    col4.metric(
        "Volatilité",
        f"{metrics['Volatilité (%)']}%"
    )

    col5.metric(
        "Drawdown",
        f"{metrics['Drawdown Max (%)']}%"
    )

    st.subheader("Historique")

    st.line_chart(
        df["Close"]
    )

    st.subheader("Commentaire automatique")

    st.info(
        generate_commentary(metrics)
    )

    st.subheader("Dernières données")

    st.dataframe
