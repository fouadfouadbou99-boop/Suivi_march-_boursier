import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

from reporting import (
    generate_excel_report
)

st.set_page_config(
    page_title="CMR - Suivi des Indices",
    layout="wide"
)

st.title("CMR - Suivi des Indices")

# ======================================
# IMPORT EXCEL
# ======================================

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

# ======================================
# CHOIX DU MARCHE
# ======================================

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

    # ======================================
    # KPI MARCHE
    # ======================================

    st.subheader(
        "Indicateurs de marché"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Plus Haut",
        f"{metrics['Plus Haut']:,.2f}"
    )

    c2.metric(
        "Plus Bas",
        f"{metrics['Plus Bas']:,.2f}"
    )

    c3.metric(
        "Distance Plus Haut",
        f"{metrics['Distance Plus Haut (%)']}%"
    )

    st.divider()

    c4, c5, c6, c7, c8, c9 = st.columns(6)

    c4.metric(
        "MTD",
        f"{metrics['MTD (%)']}%"
    )

    c5.metric(
        "YTD",
        f"{metrics['YTD (%)']}%"
    )

    c6.metric(
        "1 An",
        "N/D"
        if metrics["1 An (%)"] is None
        else f"{metrics['1 An (%)']}%"
    )

    c7.metric(
        "3 Ans Ann.",
        "N/D"
        if metrics["3 Ans Ann. (%)"] is None
        else f"{metrics
