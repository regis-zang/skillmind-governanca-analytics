import streamlit as st
import pandas as pd

from src.skillmind_dashboard.data_loader import load_base
from src.skillmind_dashboard.ui import render_sidebar


# Configuração da página
st.set_page_config(
    page_title="SkillMind Governança – Dashboard",
    layout="wide"
)

# Sidebar com branding + filtros
filters = render_sidebar()

# Carregar base
df = load_base()

# ============================
# APLICAR FILTROS GLOBAIS
# ============================

# Filtro por período (Data de abertura)
if (
    "Data de abertura" in df.columns
    and filters.get("date_range")
    and len(filters["date_range"]) == 2
):
    inicio, fim = filters["date_range"]
    inicio = pd.to_datetime(inicio)
    fim = pd.to_datetime(fim)

    df = df[
        (df["Data de abertura"] >= inicio)
        & (df["Data de abertura"] <= fim)
    ]

# Filtro por Categoria
if "Categoria" in df.columns and filters.get("categoria"):
    df = df[df["Categoria"].isin(filters["categoria"])]

# Filtro por Rota SkillMind
if "Rota_SkillMind" in df.columns and filters.get("rota"):
    df = df[df["Rota_SkillMind"].isin(filters["rota"])]

# ============================
# CONTEÚDO DA PÁGINA PRINCIPAL
# ============================

st.title("📊 SkillMind – Governança de Chamados")
st.markdown(
    "Visão geral dos chamados considerando os filtros aplicados no menu lateral."
)

# KPIs principais
col1, col2, col3 = st.columns(3)

# Total de chamados
col1.metric("Total de Chamados", len(df))

# SLA atrasado (%)
if "sla_atrasado" in df.columns:
    sla_series = pd.to_numeric(df["sla_atrasado"], errors="coerce")
    sla_pct = sla_series.mean() * 100
    col2.metric("SLA Atrasado (%)", f"{sla_pct:.2f}%")
else:
    col2.write("Coluna `sla_atrasado` não encontrada na base.")

# Tempo médio de resolução (horas)
if "tempo_resolucao_horas" in df.columns:
    tempo_series = pd.to_numeric(df["tempo_resolucao_horas"], errors="coerce")
    tempo_medio = tempo_series.mean()
    col3.metric("Tempo Médio (horas)", f"{tempo_medio:.2f}")
else:
    col3.write("Coluna `tempo_resolucao_horas` não encontrada na base.")

st.markdown("### 📄 Prévia da Base Filtrada")
st.dataframe(df.head())

st.caption(
    "Os números acima refletem apenas os chamados dentro do período, categorias e rotas selecionados no filtro."
)
