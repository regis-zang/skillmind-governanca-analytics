import streamlit as st
import pandas as pd
import plotly.express as px

from src.skillmind_dashboard.data_loader import load_base
from src.skillmind_dashboard.ui import render_sidebar

st.title("⏱️ SLA & Tempos de Resolução")

filters = render_sidebar()
df = load_base()

# Aplicar filtros
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

# Métricas
col1, col2 = st.columns(2)

if "tempo_resolucao_horas" in df.columns:
    col1.metric("Tempo Médio (horas)", f"{df['tempo_resolucao_horas'].mean():.2f}")

if "sla_atrasado" in df.columns:
    col2.metric("SLA Atrasado (%)", f"{df['sla_atrasado'].mean() * 100:.2f}%")

# Gráfico
if "tempo_resolucao_horas" in df.columns:
    fig = px.histogram(
        df,
        x="tempo_resolucao_horas",
        nbins=40,
        title="Distribuição dos Tempos de Resolução",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'tempo_resolucao_horas' não encontrada.")
