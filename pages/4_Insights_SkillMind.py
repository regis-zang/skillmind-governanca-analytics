import streamlit as st
import pandas as pd
from src.skillmind_dashboard.data_loader import load_base
from src.skillmind_dashboard.ui import render_sidebar

st.title("🧠 Insights SkillMind")

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

st.markdown("### 🔍 Insights automáticos gerados com base nos dados filtrados")

insights = []

# SLA atrasado
if "sla_atrasado" in df.columns:
    sla = df["sla_atrasado"].mean()
    if sla > 0.15:
        insights.append("⚠️ O percentual de SLA atrasado está acima de 15%. Revisar filas críticas.")

# Tempo médio
if "tempo_resolucao_horas" in df.columns:
    tempo = df["tempo_resolucao_horas"].mean()
    if tempo > 48:
        insights.append("⏱️ Tempo médio acima de 48 horas, indicando gargalos no suporte.")

# Top categorias
if "Categoria" in df.columns:
    top3 = df["Categoria"].value_counts().head(3).index.tolist()
    insights.append(f"📌 Categorias mais frequentes: **{', '.join(top3)}**")

# Rota mais acionada
if "Rota_SkillMind" in df.columns:
    rota_max = df["Rota_SkillMind"].value_counts().idxmax()
    insights.append(f"🧭 Rota SkillMind mais utilizada: **{rota_max}**")

# Exibir insights
for i in insights:
    st.write(i)

if not insights:
    st.info("Nenhum insight disponível para os filtros atuais.")
