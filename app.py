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

st.title(
    "CMR - Suivi des Indices"
)

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

    st.subheader(
        "Indicateurs"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "MTD",
        f"{metrics['MTD (%)']}%"
    )

    col2.metric(
        "YTD",
        f"{metrics['YTD (%)']}%"
    )

    col3.metric(
        "Volatilité",
        f"{metrics['Volatilité (%)']}%"
    )

    col4.metric(
        "Drawdown",
        f"{metrics['Drawdown Max (%)']}%"
    )

    st.subheader(
        "Historique"
    )

    st.line_chart(
        df["Close"]
    )

    st.subheader(
        "Commentaire automatique"
    )

    st.info(
        generate_commentary(
            metrics
        )
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
