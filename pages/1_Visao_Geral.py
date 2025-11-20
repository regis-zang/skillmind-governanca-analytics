import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# Garantir que a pasta src/ esteja no PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from skillmind_dashboard.data_loader import load_base
from skillmind_dashboard.ui import render_sidebar


st.title("📊 Visão Geral dos Chamados")

# Sidebar + filtros
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

# ============================
# Chamados por mês
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

# ============================
# Chamados por Entidade
# ============================

if "Entidade" in df.columns:
    st.markdown("### 🏢 Chamados por Entidade")
    ent = df["Entidade"].value_counts().reset_index()
    ent.columns = ["Entidade", "Total"]

    fig2 = px.bar(
        ent.head(15),
        x="Entidade",
        y="Total",
        title="Top Entidades por quantidade de chamados",
    )
    st.plotly_chart(fig2, use_container_width=True)
