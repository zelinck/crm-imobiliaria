"""
app.py — Entry point do CRM Imobiliária MCMV (Módulo 1: Financiamento)
"""

import streamlit as st

st.set_page_config(
    page_title="CRM Imobiliária MCMV",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Estilo global ----------
st.markdown("""
<style>
    [data-testid="stSidebarNav"] { font-size: 15px; }
    /* ── Habitare palette: primary #2F5AA8 ── */
    .metric-card {
        background: #0e2144;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 4px solid #2F5AA8;
        margin-bottom: 8px;
        color: #ffffff;
    }
    .etapa-badge {
        display: inline-block;
        background: #2F5AA8;
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-pendente   { background:#fff3cd; color:#856404; padding:2px 8px; border-radius:12px; font-size:12px; }
    .badge-enviado    { background:#b8d4f5; color:#0d2d5a; padding:2px 8px; border-radius:12px; font-size:12px; }
    .badge-aprovado   { background:#c8ead8; color:#0a3622; padding:2px 8px; border-radius:12px; font-size:12px; }
    .badge-rejeitado  { background:#f8d7da; color:#842029; padding:2px 8px; border-radius:12px; font-size:12px; }
    .tabela-linha {
        border-bottom: 1px solid #1e3060;
        padding: 8px 4px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Usuário logado (simples, sem auth) ----------
if "usuario" not in st.session_state:
    st.session_state.usuario = "Usuário"

with st.sidebar:
    try:
        st.image("https://storage.googleapis.com/imobzi/accounts/ac-sjtw19114w3f5/public/logo2.png", use_column_width=True)
    except Exception:
        st.markdown("### 🏠 Habitare")
    st.markdown("---")
    usuario = st.text_input("Seu nome", value=st.session_state.usuario, key="input_usuario")
    st.session_state.usuario = usuario
    st.markdown("---")
    st.caption("Módulo 1 — Financiamento MCMV")

# ---------- Home ----------
st.title("🏠 CRM Imobiliária MCMV")
st.markdown("### Módulo 1 — Correspondente Caixa / Financiamento")

try:
    from database import contar_por_etapa, alertas_credito_vencendo, ETAPAS_ATIVAS

    col1, col2, col3, col4 = st.columns(4)
    contagem = contar_por_etapa()

    total_ativos = sum(v for k, v in contagem.items() if k in ETAPAS_ATIVAS)
    concluidos   = contagem.get("Concluído", 0)
    reprovados   = contagem.get("Crédito Reprovado", 0)
    alertas      = len(alertas_credito_vencendo(30))

    col1.metric("Clientes ativos", total_ativos)
    col2.metric("Financiamentos concluídos", concluidos)
    col3.metric("Créditos reprovados", reprovados)
    col4.metric("⚠️ Alertas (crédito)", alertas, delta=f"vencem em 30 dias", delta_color="inverse")

    st.markdown("---")
    st.markdown("#### Distribuição por etapa")

    cols = st.columns(len(ETAPAS_ATIVAS))
    for i, etapa in enumerate(ETAPAS_ATIVAS):
        n = contagem.get(etapa, 0)
        cols[i].markdown(
            f"<div class='metric-card'><b style='font-size:1.4em'>{n}</b><br><small>{etapa}</small></div>",
            unsafe_allow_html=True
        )

except Exception as e:
    st.info("Configure as credenciais do Supabase em `.streamlit/secrets.toml` para começar.")
    st.caption(f"Detalhe: {e}")

st.markdown("---")
st.markdown(
    "Use o menu lateral para navegar: **Pipeline**, **Clientes**, **Novo Cliente** ou **Alertas**."
)
