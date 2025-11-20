import streamlit as st
from src.skillmind_dashboard.data_loader import load_base
import plotly.express as px

st.title("🧩 Categorias e Rotas SkillMind")

df = load_base()

# Categoria
st.markdown("### Chamados por Categoria")
if "Categoria" in df.columns:
    fig = px.bar(
        df.groupby("Categoria").size().reset_index(name="total"),
        x="Categoria",
        y="total",
        title="Distribuição por Categoria"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'Categoria' não encontrada.")

# Rota SkillMind
st.markdown("### Chamados por Rota SkillMind")
if "Rota_SkillMind" in df.columns:
    fig = px.pie(
        df,
        names="Rota_SkillMind",
        title="Distribuição por Rota"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'Rota_SkillMind' não encontrada.")
