import streamlit as st
from src.skillmind_dashboard.data_loader import load_base

def render_sidebar():
    st.sidebar.markdown(
        """
        <div style="padding:10px; text-align:center;">
            <h2 style="margin-bottom:0;">🧠 SkillMind</h2>
            <p style="margin-top:0;">Governança & Analytics</p>
        </div>
        <hr>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.subheader("🔎 Filtros")

    df = load_base()

    # Período
    if "Data de abertura" in df.columns:
        min_date = df["Data de abertura"].min()
        max_date = df["Data de abertura"].max()

        date_range = st.sidebar.date_input(
            "Período",
            value=(min_date, max_date)
        )
    else:
        date_range = None

    # Categoria
    categoria = None
    if "Categoria" in df.columns:
        categoria = st.sidebar.multiselect(
            "Categoria",
            sorted(df["Categoria"].dropna().unique())
        )

    # Rota
    rota = None
    if "Rota_SkillMind" in df.columns:
        rota = st.sidebar.multiselect(
            "Rota SkillMind",
            sorted(df["Rota_SkillMind"].dropna().unique())
        )

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.caption("Versão 0.1.0 • FIAP • SkillMind Engine")

    # Retornar filtros para as páginas
    return {
        "date_range": date_range,
        "categoria": categoria,
        "rota": rota
    }
