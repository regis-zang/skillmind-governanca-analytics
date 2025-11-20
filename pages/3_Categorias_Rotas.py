import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from skillmind_dashboard.data_loader import load_base
from skillmind_dashboard.ui import render_sidebar


st.title("🧩 Categorias e Rotas SkillMind")

filters = render_sidebar()
df = load_base()

# Aplicar filtros
if (
    "Data de abertura" in df.columns
    and filters.get("date_range")
    and len(filters["date_range"]) == 2
):
    inicio, fim = filters["date_range"]
    inicio = pd.to_datetime(inicio)
    fim = pd.to_datetime(fim)
    df = df[(df["Data de abertura"] >= inicio) & (df["Data de abertura"] <= fim)]

if "Categoria" in df.columns and filters.get("categoria"):
    df = df[df["Categoria"].isin(filters["categoria"])]

if "Rota_SkillMind" in df.columns and filters.get("rota"):
    df = df[df["Rota_SkillMind"].isin(filters["rota"])]

# Categorias
st.markdown("### 📂 Chamados por Categoria")
if "Categoria" in df.columns:
    cat_counts = df["Categoria"].value_counts().reset_index()
    cat_counts.columns = ["Categoria", "Total"]

    fig_cat = px.bar(
        cat_counts,
        x="Categoria",
        y="Total",
        title="Distribuição por Categoria",
    )
    st.plotly_chart(fig_cat, use_container_width=True)
else:
    st.warning("Coluna 'Categoria' não encontrada.")

# Rotas SkillMind
st.markdown("### 🧭 Rotas SkillMind")
if "Rota_SkillMind" in df.columns:
    fig_rota = px.pie(
        df,
        names="Rota_SkillMind",
        title="Distribuição por Rota SkillMind",
    )
    st.plotly_chart(fig_rota, use_container_width=True)
else:
    st.warning("Coluna 'Rota_SkillMind' não encontrada.")
