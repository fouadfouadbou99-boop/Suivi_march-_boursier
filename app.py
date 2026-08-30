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

    st.caption(
        f"Dernière mise à jour : {df.index[-1].strftime('%d/%m/%Y')}"
    )

    st.metric(
        "Niveau actuel du MASI",
        f"{df['Close'].iloc[-1]:,.2f}"
    )

    metrics = compute_metrics(df)

    st.subheader("Indicateurs de marché")

    a, b, c = st.columns(3)

    a.metric(
        "Plus Haut",
        f"{metrics['Plus Haut']:,.2f}"
    )

    b.metric(
        "Plus Bas",
        f"{metrics['Plus Bas']:,.2f}"
    )

    c.metric(
        "Distance Plus Haut",
        f"{metrics['Distance Plus Haut (%)']}%"
    )

    st.divider()

    d, e, f, g, h, i = st.columns(6)

    d.metric(
        "MTD",
        f"{metrics['MTD (%)']}%"
    )

    e.metric(
        "YTD",
        f"{metrics['YTD (%)']}%"
    )

    f.metric(
        "1 An",
        "N/D"
        if metrics["1 An (%)"] is None
        else f"{metrics['1 An (%)']}%"
    )

    g.metric(
        "3 Ans Ann.",
        "N/D"
        if metrics["3 Ans Ann. (%)"] is None
        else f"{metrics['3 Ans Ann. (%)']}%"
    )

    h.metric(
        "Volatilité",
        f"{metrics['Volatilité (%)']}%"
    )

    i.metric(
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
