# SkillMind Governança Analytics

Dashboard analítico para suporte ao projeto **SkillMind**, focado em governança de chamados, SLA, categorias, rotas e insights operacionais.

Este repositório consolida o pipeline de dados (arquivo `.parquet`) e a aplicação em **Streamlit** para visualização interativa.

---

## 🚀 Objetivo
Entregar uma visão analítica completa sobre:
- Volumetria de chamados
- Tempo médio de solução
- SLA por categoria e urgência
- Análises de rotas (Rota_SkillMind)
- Insights para governança e capacitação

---

## 📂 Estrutura do projeto

###📦 requirements.txt
🧠 Por que cada biblioteca?
Biblioteca	Motivo
streamlit	app principal do dashboard
pandas	manipulação de dados
pyarrow	leitura de parquet com performance
plotly	gráficos modernos e interativos
matplotlib	gráfico simples (SLA, barras) se quiser
numpy	base matemática para KPIs
python-dateutil	manipulação flexível de datas / períodos


