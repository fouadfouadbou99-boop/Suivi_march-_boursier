import streamlit as st
import pandas as pd

from market import (
    load_data,
    compute_metrics,
    generate_commentary
)

st.set_page_config(
    page_title="CMR Suivi Indices"
)

st.title("CMR - Suivi des Indices")

symbol = st.text_input(
    "Indice Yahoo",
    "^FCHI"
)

try:

    df = load_data(symbol)

    if df.empty:
        st.error("Aucune donnée récupérée.")
        st.stop()

    metrics = compute_metrics(df)

    st.dataframe(
        pd.DataFrame([metrics])
    )

    close = df["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    st.line_chart(close)

    st.text(
        generate_commentary(
            symbol,
            metrics
        )
    )

except Exception as e:

    st.error(str(e))
