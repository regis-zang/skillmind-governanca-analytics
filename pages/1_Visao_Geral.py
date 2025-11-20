import streamlit as st
import pandas as pd
import plotly.express as px

from src.skillmind_dashboard.data_loader import load_base
from src.skillmind_dashboard.ui import render_sidebar

st.title("📊 Visão Geral dos Chamados")

# Sidebar + filtros
filters = render_sidebar()

df = load_base()

# ============================
# Aplicar filtros
# ============================

if "Data de abertura" in df.columns and filters.get("date_range"):
    inicio, fim = filters["date_range"]
    inicio = pd.to_datetime(inicio)
    fim = pd.to_datetime(fim)
    df = df[(df["Data de abertura"] >= inicio) & (df["Data de abertura"] <= fim)]

if "Categoria" in df.columns and filters.get("categoria"):
    df = df[df["Categoria"].isin(filters["categoria"])]

if "Rota_SkillMind" in df.columns and filters.get("rota"):
    df = df[df["Rota_SkillMind"].isin(filters["rota"])]

# ============================
# Conteúdo
# ============================

st.markdown("### 📅 Chamados por mês")

if "Data de abertura" in df.columns:
    df["mes"] = df["Data de abertura"].dt.to_period("M").astype(str)
    mensal = df.groupby("mes").size().reset_index(name="total")

    fig = px.bar(
        mensal,
        x="mes",
        y="total",
        title="Volume de Chamados por Mês",
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Coluna 'Data de abertura' não encontrada.")

st.markdown("### 🧩 Distribuição por Categoria")
if "Categoria" in df.columns:
    categoria = df["Categoria"].value_counts().reset_index()
    categoria.columns = ["Categoria", "Total"]

    fig2 = px.bar(
        categoria,
        x="Categoria",
        y="Total",
        title="Chamados por Categoria",
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Coluna 'Categoria' não encontrada.")
