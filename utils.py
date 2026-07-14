TEST"""
utils.py — Helpers compartilhados: tema, sidebar, constantes de cores
"""
import streamlit as st

LOGO_URL = "https://storage.googleapis.com/imobzi/accounts/ac-sjtw19114w3f5/public/logo2.png"

HAB_PRIMARY = "#2F5AA8"
HAB_BG      = "#F0F4F8"
HAB_CARD    = "#FFFFFF"

# Cor de cada etapa
COR_ETAPA = {
    "Lead":                    "#4A90D9",
    "Análise de Crédito":      "#F39C12",
    "Crédito Reprovado":       "#E74C3C",
    "Crédito Aprovado":        "#27AE60",
    "Abertura de Conta":       "#8E44AD",
    "Documentação Engenharia": "#2980B9",
    "SIOP":                    "#16A085",
    "Assinatura Digital":      "#E67E22",
    "Análise Digital":         "#C0392B",
    "Assinatura Contrato":     "#1ABC9C",
    "Cartório":                "#2ECC71",
    "Concluído":               "#27AE60",
}

LIGHT_CSS = """
<style>
/* ── Base ── */
[data-testid="stAppViewContainer"] > .main { background: #F0F4F8; }
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #DDE3EE;
}

/* Oculta nav padrão do Streamlit */
[data-testid="stSidebarNav"] { display: none !important; }

/* Sidebar nav links customizados */
[data-testid="stSidebar"] [data-testid="stPageLink"] a,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    display: flex !important;
    align-items: center;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    color: #3A4A6B !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    transition: background 0.15s !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: #EDF3FF !important;
    color: #2F5AA8 !important;
}

/* Cards brancos genéricos */
.card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}

/* Separadores */
hr { border: none !important; border-top: 1px solid #E5EAF2 !important; }

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select {
    border-radius: 8px !important;
    border: 1px solid #DDE3EE !important;
    background: #FFFFFF !important;
}

/* Botões primários */
button[kind="primary"] {
    background: #2F5AA8 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
button[kind="secondary"] {
    border-radius: 8px !important;
    border: 1px solid #DDE3EE !important;
    color: #3A4A6B !important;
}

/* Títulos */
h1, h2, h3 { color: #1A2035 !important; }
</style>
"""


def render_sidebar():
    """Renderiza sidebar padrão com logo + nav com ícones + campo de usuário."""
    with st.sidebar:
        try:
            st.image(LOGO_URL, use_column_width=True)
        except Exception:
            st.markdown("### 🏠 Habitare")

        st.markdown("<br>", unsafe_allow_html=True)

        # Navegação com ícones
        st.page_link("app.py",                  label="🏠  Dashboard")
        st.page_link("pages/1_Pipeline.py",      label="📋  Pipeline")
        st.page_link("pages/2_Clientes.py",      label="👥  Clientes")
        st.page_link("pages/3_Novo_Cliente.py",  label="➕  Novo Cliente")
        st.page_link(pages/4_Alertas.py",       label="⚠️  Alertas")

        st.markdown("---")
        usuario = st.text_input(
            "👤 Seu nome",
            value=st.session_state.get("usuario", "Usuário"),
            key="input_usuario_sidebar",
        )
        st.session_state["usuario"] = usuario

        st.markdown("---")
        st.caption("Habitare Imobiliária · Módulo 1\nFinanciamento MCMV")
"""
utils.py — Helpers compartilhados: tema, sidebar, constantes de cores
"""
import streamlit as st

LOGO_URL = "https://storage.googleapis.com/imobzi/accounts/ac-sjtw19114w3f5/public/logo2.png"

HAB_PRIMARY = "#2F5AA8"
HAB_BG      = "#F0F4F8"
HAB_CARD    = "#FFFFFF"

# Cor de cada etapa
COR_ETAPA = {
    "Lead":                    "#4A90D9",
    "Análise de Crédito":      "#F39C12",
    "Crédito Reprovado":       "#E74C3C",
    "Crédito Aprovado":        "#27AE60",
    "Abertura de Conta":       "#8E44AD",
    "Documentação Engenharia": "#2980B9",
    "SIOP":                    "#16A085",
    "Assinatura Digital":      "#E67E22",
    "Análise Digital":         "#C0392B",
    "Assinatura Contrato":     "#1ABC9C",
    "Cartório":                "#2ECC71",
    "Concluído":               "#27AE60",
}

LIGHT_CSS = """
<style>
/* ── Base ── */
[data-testid="stAppViewContainer"] > .main { background: #F0F4F8; }
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #DDE3EE;
}

/* Oculta nav padrão do Streamlit */
[data-testid="stSidebarNav"] { display: none !important; }

/* Sidebar nav links customizados */
[data-testid="stSidebar"] [data-testid="stPageLink"] a,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    display: flex !important;
    align-items: center;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    color: #3A4A6B !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    transition: background 0.15s !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: #EDF3FF !important;
    color: #2F5AA8 !important;
}

/* Cards brancos genéricos */
.card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}

/* Separadores */
hr { border: none !important; border-top: 1px solid #E5EAF2 !important; }

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select {
    border-radius: 8px !important;
    border: 1px solid #DDE3EE !important;
    background: #FFFFFF !important;
}

/* Botões primários */
button[kind="primary"] {
    background: #2F5AA8 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
button[kind="secondary"] {
    border-radius: 8px !important;
    border: 1px solid #DDE3EE !important;
    color: #3A4A6B !important;
}

/* Títulos */
h1, h2, h3 { color: #1A2035 !important; }
</style>
"""


def render_sidebar():
    """Renderiza sidebar padrão com logo + nav com ícones + campo de usuário."""
    with st.sidebar:
        try:
            st.image(LOGO_URL, use_column_width=True)
        except Exception:
            st.markdown("### 🏠 Habitare")

        st.markdown("<br>", unsafe_allow_html=True)

        # Navegação com ícones
        st.page_link("app.py",                  label="🏠  Dashboard")
        st.page_link("pages/1_Pipeline.py",      label="📋  Pipeline")
        st.page_link("pages/2_Clientes.py",      label="👥  Clientes")
        st.page_link("pages/3_Novo_Cliente.py",  label="➕  Novo Cliente")
        st.page_link("pages/4_Alertas.py",       label="⚠️  Alertas")

        st.markdown("---")
        usuario = st.text_input(
            "👤 Seu nome",
            value=st.session_state.get("usuario", "Usuário"),
            key="input_usuario_sidebar",
        )
        st.session_state["usuario"] = usuario

        st.markdown("---")
        st.caption("Habitare Imobiliária · Módulo 1\nFinanciamento MCMV")
