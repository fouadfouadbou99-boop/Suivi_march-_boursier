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

    # ======================================
    # INFORMATIONS GENERALES
    # ======================================

    st.caption(
        f"Dernière mise à jour : "
        f"{df.index[-1].strftime('%d/%m/%Y')}"
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
        else f"{metrics['3 Ans Ann. (%)']}%"
    )

    c8.metric(
        "Volatilité",
        f"{metrics['Volatilité (%)']}%"
    )

    c9.metric(
        "Drawdown",
        f"{metrics['Drawdown Max (%)']}%"
    )

    # ======================================
    # GRAPHIQUE PLOTLY
    # ======================================

    st.subheader(
        "Historique du MASI"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="MASI",
            line=dict(
                width=3
            )
        )
    )

    fig.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="Niveau de l'indice",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ======================================
    # COMMENTAIRE
    # ======================================

    st.subheader(
        "Commentaire automatique"
    )

    st.info(
        generate_commentary(metrics)
    )

    # ======================================
    # DONNEES
    # ======================================

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
