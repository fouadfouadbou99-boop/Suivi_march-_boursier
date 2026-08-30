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

# ==================================
# IMPORT EXCEL
# ==================================

st.sidebar.header(
    "Mise à jour des données"
)

uploaded_file = st.sidebar.file_uploader(
    "Importer Data_masi.xlsx",
    type=["xlsx"]
)

if uploaded_file is not None:

    st.sidebar.success(
        "Fichier chargé avec succès"
    )

# ==================================
# CHOIX DU MARCHE
# ==================================

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

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "MTD",
        f"{metrics['MTD (%)']}%"
    )

    col2.metric(
        "YTD",
        f"{metrics['YTD (%)']}%"
    )

    if metrics["1 An (%)"] is None:

        col3.metric(
            "1 An",
            "N/D"
        )

    else:

        col3.metric(
            "1 An",
            f"{metrics['1 An (%)']}%"
        )

    if metrics["3 Ans Ann. (%)"] is None:

        col4.metric(
            "3 Ans Ann.",
            "N/D"
        )

    else:

        col4.metric(
            "3 Ans Ann.",
            f"{metrics['3 Ans Ann. (%)']}%"
        )

    col5.metric(
        "Volatilité",
        f"{metrics['Volatilité (%)']}%"
    )

    col6.metric(
        "Drawdown",
        f"{metrics['Drawdown Max (%)']}%"
    )

    st.subheader("Historique")

    st.line_chart(
        df["Close"]
    )

    st.subheader(
        "Commentaire automatique"
    )

    st.info(
        generate_commentary(metrics)
    )

    st.subheader(
        "10 dernières observations"
    )

    st.dataframe(
        df.tail(10)
    )

except Exception as e:

    st.error(
        f"Erreur : {e}"
    )
