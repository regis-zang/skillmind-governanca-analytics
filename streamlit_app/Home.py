import streamlit as st
from src.skillmind_dashboard.data_loader import load_base

st.set_page_config(
    page_title="SkillMind Governança – Dashboard",
    layout="wide"
)

st.title("📊 SkillMind – Governança de Chamados")

# Carregar dados
df = load_base()

# KPIs principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Chamados", len(df))
col2.metric("SLA Atrasado (%)", f"{df['sla_atrasado'].mean() * 100:.2f}%")
col3.metric("Tempo Médio (horas)", f"{df['tempo_resolucao_horas'].mean():.2f}")

# Preview
st.subheader("📄 Prévia da Base")
st.dataframe(df.head())
