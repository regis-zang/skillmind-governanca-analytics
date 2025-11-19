import streamlit as st
from src.skillmind_dashboard.data_loader import load_base
import plotly.express as px

st.title("📊 Visão Geral dos Chamados")

df = load_base()

st.markdown("### Volumetria por mês")

# Criar coluna de mês se existir data de abertura
if "Data de abertura" in df.columns:
    df["mes"] = df["Data de abertura"].dt.to_period("M").astype(str)
    fig = px.bar(
        df.groupby("mes").size().reset_index(name="total"),
        x="mes",
        y="total",
        title="Chamados por mês"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'Data de abertura' não encontrada na base.")

st.markdown("### Distribuição por Categoria")
if "Categoria" in df.columns:
    fig = px.histogram(
        df,
        x="Categoria",
        title="Chamados por categoria",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'Categoria' não encontrada na base.")
