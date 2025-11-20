import streamlit as st
from src.skillmind_dashboard.data_loader import load_base

st.title("🧠 Insights SkillMind")

df = load_base()

st.markdown("### Recomendações iniciais baseadas na análise")

insights = []

if "sla_atrasado" in df.columns:
    atraso = df["sla_atrasado"].mean()
    if atraso > 0.15:
        insights.append("⚠️ Alto percentual de SLA atrasado — recomenda-se revisar filas críticas.")

if "tempo_resolucao_horas" in df.columns:
    tempo = df["tempo_resolucao_horas"].mean()
    if tempo > 60:
        insights.append("⏱️ Tempo médio elevado — possível gargalo de atendimento.")

if "Categoria" in df.columns:
    categorias_top = df["Categoria"].value_counts().head(3)
    insights.append(f"📌 Categorias mais frequentes: **{', '.join(categorias_top.index)}**")

if "Rota_SkillMind" in df.columns:
    rotas_top = df["Rota_SkillMind"].value_counts().idxmax()
    insights.append(f"🧭 Rota mais acionada: **{rotas_top}**")

# Exibe insights
for item in insights:
    st.write(item)

if not insights:
    st.info("Nenhum insight gerado — verifique se as colunas esperadas existem na base.")
