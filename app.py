import streamlit as st

from market import (
    load_yahoo_data,
    compute_performance
)

from technical import (
    moving_averages
)

from risk import (
    volatility,
    max_drawdown
)

from commentary import (
    generate_commentary
)

from config import INDICES

st.set_page_config(
    page_title="CMR Marchés",
    layout="wide"
)

st.title(
    "CMR - Suivi des Marchés"
)

nom = st.selectbox(
    "Indice",
    list(INDICES.keys())
)

ticker = INDICES[nom]

df = load_yahoo_data(ticker)

close = df["Close"]

if hasattr(close, "columns"):
    close = close.iloc[:, 0]

perf = compute_performance(df)

vol = volatility(close)

dd = max_drawdown(close)

ma = moving_averages(close)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Performance YTD",
    f"{perf['YTD']:.2f}%"
)

c2.metric(
    "Volatilité",
    f"{vol:.2f}%"
)

c3.metric(
    "Drawdown Max",
    f"{dd:.2f}%"
)

st.line_chart(close)

st.subheader(
    "Moyennes Mobiles"
)

st.write(ma)

st.subheader(
    "Commentaire"
)

st.write(
    generate_commentary(
        nom,
        perf["YTD"],
        vol
    )
)
