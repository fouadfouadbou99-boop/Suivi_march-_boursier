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

# ===================================
# IMPORT D'UN NOUVEAU FICHIER MASI
# ===================================

st.sidebar.header("Mise à jour des données")

uploaded_file = st.sidebar.file_uploader(
    "Importer Data_masi.xlsx",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

        nouveau_df = pd.read_excel(
            uploaded_file
        )

        st.sidebar.success(
            "Fichier chargé avec succès"
        )

    except Exception as e:

        st.sidebar.error(
            f"Erreur : {e}"
        )

# ===================================
# CHOIX DU MARCHÉ
# ===================================

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

    # ===================================
    # KPI
    # ===================================

    st.subheader("Indicateurs")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "MTD",
        f"{metrics['MTD (%)']}%"
    )

    col2.metric(
        "QTD",
        f"{metrics['QTD (%)']}%"
    )

    col3.metric(
        "YTD",
        f"{metrics['YTD (%)']}%"
    )

    col4.metric(
        "Volatilité",
        f"{metrics['Volatilité (%)']}%"
    )

    col5.metric(
        "Drawdown",
        f"{metrics['Drawdown Max (%)']}%"
    )

    # ===================================
    # GRAPHIQUE
    # ===================================

    st.subheader("Historique")

    st.line_chart(
        df["Close"]
    )

    # ===================================
    # COMMENTAIRE
    # ===================================

    st.subheader(
        "Commentaire automatique"
    )

    st.info(
        generate_commentary(metrics)
    )

    # ===================================
    # DERNIERES VALEURS
    # ===================================

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
