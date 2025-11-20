import streamlit as st
import plotly.express as px
import pandas as pd

from src.skillmind_dashboard.data_loader import load_base
from src.skillmind_dashboard.ui import render_sidebar

st.title("🧩 Categorias e Rotas SkillMind")

filters = render_sidebar()
df = load_base()

# Aplicar filtros globais
if "Data de abertura" in df.columns and filters.get("date_range"):
    inicio, fim = filters["date_range"]
    df = df[
        (df["Data de abertura"] >= pd.to_datetime(inicio)) &
        (df["Data de abertura"] <= pd.to_datetime(fim))
    ]

if "Categoria" in df.columns and filters.get("categoria"):
    df = df[df["Categoria"].isin(filters["categoria"])]

if "Rota_SkillMind" in df.columns and filters.get("rota"):
    df = df[df["Rota_SkillMind"].isin(filters["rota"])]

# Categoria
st.markdown("### Categoria")
if "Categoria" in df.columns:
    fig_cat = px.bar(
        df["Categoria"].value_counts(),
        title="Chamados por Categoria"
    )
    st.plotly_chart(fig_cat, use_container_width=True)
else:
    st.warning("Coluna 'Categoria' não encontrada.")

# Rota SkillMind
st.markdown("### Rotas SkillMind")
if "Rota_SkillMind" in df.columns:
    fig_rota = px.pie(
        df,
        names="Rota_SkillMind",
        title="Distribuição por Rota SkillMind"
    )
    st.plotly_chart(fig_rota, use_container_width=True)
else:
    st.warning("Coluna 'Rota_SkillMind' não encontrada.")
