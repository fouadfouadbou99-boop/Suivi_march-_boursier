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

# ====================================================
# IMPORT FICHIER
# ====================================================

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

# ====================================================
# CHOIX DU MARCHÉ
# ====================================================

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

        if uploaded_file is not None:

            df = pd.read_excel(uploaded_file)

            if "Date" not in df.columns:
                st.error(
                    "Colonne Date introuvable"
                )
                st.stop()

            if "Close" not in df.columns:
                st.error(
                    "Colonne Close introuvable"
                )
                st.stop()

            df["Date"] = pd.to_datetime(
                df["Date"]
            )

            df["Close"] = (
                df["Close"]
                .astype(str)
                .str.replace(" ", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

            df["Close"] = pd.to_numeric(
                df["Close"],
                errors="coerce"
            )

            df = df.dropna(
                subset=["Close"]
            )

            df = df.sort_values(
                "Date"
            )

            df.set_index(
                "Date",
                inplace=True
            )

        else:

            df = load_maroc_index(
                MAROC_INDICES[indice]
            )

            df["Close"] = (
                df["Close"]
                .astype(str)
                .str.replace(" ", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

            df["Close"] = pd.to_numeric(
                df["Close"],
                errors="coerce"
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

    st.caption(
        f"Dernière mise à jour : {df.index[-1].strftime('%d/%m/%Y')}"
    )

    st.metric(
        "Niveau actuel du MASI",
        f"{df['Close'].iloc[-1]:,.2f}"
    )

    st.subheader(
        "Analyse Technique"
    )

    t1, t2 = st.columns(2)

    t1.metric(
        "MM20",
        f"{metrics['MM20']:,.2f}"
    )

    t2.metric(
        "MM52",
        f"{metrics['MM52']:,.2f}"
    )

    if metrics["Signal"] == "Haussier":
        st.success("✅ Tendance : Haussière")
    elif metrics["Signal"] == "Baissier":
        st.error("🔴 Tendance : Baissière")
    else:
        st.warning("🟠 Tendance : Neutre")

    st.subheader(
        "Indicateurs de marché"
    )

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
        "N/D" if metrics["1 An (%)"] is None
        else f"{metrics['1 An (%)']}%"
    )

    g.metric(
        "3 Ans Ann.",
        "N/D" if metrics["3 Ans Ann. (%)"] is None
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

    st.subheader(
        "Export du rapport"
    )

    fichier_excel = generate_excel_report(
        df,
        metrics
    )

    st.download_button(
        label="📊 Télécharger le rapport Excel",
        data=fichier_excel,
        file_name="Rapport_MASI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    df["MM20"] = (
        df["Close"]
        .rolling(20)
        .mean()
    )

    df["MM52"] = (
        df["Close"]
        .rolling(52)
        .mean()
    )

    st.subheader(
        "Historique du MASI"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="MASI"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MM20"],
            mode="lines",
            name="MM20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MM52"],
            mode="lines",
            name="MM52"
        )
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        width="stretch"
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
