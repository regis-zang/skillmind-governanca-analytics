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


st.title("⏱️ SLA & Tempos de Resolução")

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

col1, col2 = st.columns(2)

if "tempo_resolucao_horas" in df.columns:
    col1.metric("Tempo Médio (horas)", f"{df['tempo_resolucao_horas'].mean():.2f}")

if "sla_atrasado" in df.columns:
    col2.metric("SLA Atrasado (%)", f"{df['sla_atrasado'].mean() * 100:.2f}%")

st.markdown("### 📉 Distribuição dos tempos de resolução")

if "tempo_resolucao_horas" in df.columns:
    fig = px.histogram(
        df,
        x="tempo_resolucao_horas",
        nbins=40,
        title="Distribuição do Tempo de Resolução (horas)",
    )
    st.plotly_chart(fig, use_container_width=True)

    fig_box = px.box(
        df,
        y="tempo_resolucao_horas",
        title="Boxplot do Tempo de Resolução (horas)",
    )
    st.plotly_chart(fig_box, use_container_width=True)
else:
    st.warning("Coluna 'tempo_resolucao_horas' não encontrada.")
