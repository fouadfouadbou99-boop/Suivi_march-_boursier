import streamlit as st
import pandas as pd

from config import (
    MAROC_INDICES,
    WORLD_INDICES
)

from market import (
    load_yahoo_data,
    load_maroc_index,
    compute_metrics
)

st.set_page_config(
    page_title="CMR - Marchés",
    layout="wide"
)

st.title(
    "CMR - Suivi des Indices"
)

source = st.radio(
    "Marché",
    [
        "Maroc",
        "International"
    ]
)

if source == "Maroc":

    indice = st.selectbox(
        "Indice",
        list(MAROC_INDICES.keys())
    )

    try:
        df = load_maroc_index(
            MAROC_INDICES[indice]
        )

    except Exception as e:

        st.error(
            f"Données non disponibles : {e}"
        )

        st.stop()

else:

    indice = st.selectbox(
        "Indice",
        list(WORLD_INDICES.keys())
    )

    df = load_yahoo_data(
        WORLD_INDICES[indice]
    )

metrics = compute_metrics(df)

st.dataframe(
    pd.DataFrame([metrics])
)

st.line_chart(df["Close"])
