import sys
from pathlib import Path

import streamlit as st
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from skillmind_dashboard.data_loader import load_base
from skillmind_dashboard.ui import render_sidebar


st.title("🧠 Insights SkillMind")

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

st.markdown("### 🔍 Insights automáticos com base nos filtros atuais")

insights = []

# SLA atrasado alto
if "sla_atrasado" in df.columns:
    sla = df["sla_atrasado"].mean()
    if sla > 0.15:
        insights.append("⚠️ SLA atrasado acima de 15% — revisar filas críticas e tempos de resposta.")
    elif sla < 0.05:
        insights.append("✅ SLA atrasado abaixo de 5% — performance muito boa do time.")

# Tempo médio
if "tempo_resolucao_horas" in df.columns:
    tempo = df["tempo_resolucao_horas"].mean()
    if tempo > 72:
        insights.append("⏱️ Tempo médio acima de 72 horas — pode haver gargalos de processo ou aprovação.")
    elif tempo < 24:
        insights.append("🚀 Tempo médio abaixo de 24 horas — alta eficiência no atendimento.")

# Categorias mais frequentes
if "Categoria" in df.columns:
    top3 = df["Categoria"].value_counts().head(3).index.tolist()
    if top3:
        insights.append(f"📌 Categorias mais frequentes no período filtrado: **{', '.join(top3)}**.")

# Rota SkillMind mais utilizada
if "Rota_SkillMind" in df.columns and not df.empty:
    rota_max = df["Rota_SkillMind"].value_counts().idxmax()
    insights.append(f"🧭 Rota SkillMind mais acionada: **{rota_max}**.")

# Exibir insights
if insights:
    for msg in insights:
        st.write(msg)
else:
    st.info("Nenhum insight gerado para os filtros atuais. Ajuste o período ou as categorias para mais dados.")
