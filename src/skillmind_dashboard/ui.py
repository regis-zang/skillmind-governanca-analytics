import streamlit as st

def render_sidebar():
    st.sidebar.markdown(
        """
        <div style="padding:10px; text-align:center;">
            <h2 style="margin-bottom:0;">🧠 SkillMind</h2>
            <p style="margin-top:0;">Governança & Analytics</p>
        </div>
        <hr>
        
        ### 📌 Navegação
        
        - 📊 Visão Geral  
        - ⏱️ SLA & Tempos  
        - 🧩 Categorias & Rotas  
        - 🧠 Insights SkillMind  
        
        <hr>
        <small>Versão 0.1.0 • FIAP • SkillMind Engine</small>
        """,
        unsafe_allow_html=True
    )
