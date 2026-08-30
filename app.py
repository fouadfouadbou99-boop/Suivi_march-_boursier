import streamlit as st
import pandas as pd
import requests

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

st.sidebar.header("Administration")

if st.sidebar.button("Tester connexion Bourse Casablanca"):

    try:

        url = (
            "https://www.casablanca-bourse.com/"
            "live-market/indices/cours?symbol=MASI"
        )

        response = requests.get(
            url,
            verify=False,
            timeout=30
        )

        st.sidebar.success(
            f"Connexion OK : {response.status_code}"
        )

        st.subheader(
            "Aperçu du code source récupéré"
        )

        st.code(
            response.text[:3000]
        )

    except Exception as e:

        st.sidebar.error(
            str(e)
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

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "1 Mois",
        f"{metrics['Performance 1 mois (%)']}%"
    )

    c2.metric(
        "3 Mois",
        f"{metrics['Performance 3 mois (%)']}%"
    )

    c3.metric(
        "YTD",
        f"{metrics['Performance YTD (%)']}%"
    )

    c4.metric(
        "Volatilité",
        f"{metrics['Volatilité (%)']}%"
    )

    c5.metric(
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
        generate_commentary(metrics)
    )

except Exception as e:

    st.error(
        f"Erreur : {e}"
    )
