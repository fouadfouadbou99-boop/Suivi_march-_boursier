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
  
