import streamlit as st
import pandas as pd
from market import load_data, compute_metrics, generate_commentary
st.set_page_config(page_title="CMR Suivi Indices")
st.title("CMR - Suivi des Indices")
symbol=st.text_input("Indice Yahoo",'^FCHI')
df=load_data(symbol)
metrics=compute_metrics(df)
st.dataframe(pd.DataFrame([metrics]))
st.line_chart(df['Close'])
st.text(generate_commentary(symbol,metrics))
