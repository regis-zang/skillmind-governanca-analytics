import streamlit as st
from src.skillmind_dashboard.data_loader import load_base
import plotly.express as px

st.title("⏱️ SLA & Tempos de Resolução")

df = load_base()

col1, col2 = st.columns(2)

if "tempo_resolucao_horas" in df.columns:
    col1.metric(
        "Tempo Médio (horas)",
        f"{df['tempo_resolucao_horas'].mean():.2f}"
    )

if "sla_atrasado" in df.columns:
    col2.metric(
        "Percentual de SLA Atrasado",
        f"{df['sla_atrasado'].mean() * 100:.2f}%"
    )

# Gráfico de densidade de tempo de resolução
if "tempo_resolucao_horas" in df.columns:
    fig = px.histogram(
        df,
        x="tempo_resolucao_horas",
        nbins=40,
        title="Distribuição do Tempo de Resolução (horas)",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'tempo_resolucao_horas' não encontrada.")
