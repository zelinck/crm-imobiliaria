"""
Pipeline — visão Lista (ClickUp-style) e Kanban do funil de financiamento
"""
import streamlit as st
from datetime import date
from database import listar_clientes, listar_clientes_tabela, ETAPAS
from utils import render_sidebar, LIGHT_CSS, COR_ETAPA

st.set_page_config(page_title="Pipeline · Habitare", page_icon="📋", layout="wide")
st.markdown(LIGHT_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown(
    """
    <div style='margin-bottom:4px;'>
        <span style='font-size:22px;font-weight:700;color:#1A2035;'>📋 Pipeline</span>
        <span style='font-size:13px;color:#8899AA;margin-left:12px;'>Funil de financiamento MCMV</span>
    </div>
    """,
    unsafe_allow_html=True,
)

col_busca, col_etapa, col_view, _ = st.columns([2, 2, 2, 1])
busca        = col_busca.text_input("🔍 Buscar", placeholder="Nome do cliente...")
filtro_etapa = col_etapa.selectbox("Etapa", ["Todas"] + ETAPAS)
modo         = col_view.radio("Visualização", ["📊 Lista", "📋 Kanban"], horizontal=True)

etapa_param = None if filtro_etapa == "Todas" else filtro_etapa

st.markdown("<hr style='margin:10px 0 20px;'>", unsafe_allow_html=True)

if modo == "📊 Lista":
    clientes_tab = listar_clientes_tabela()

    if busca:
        clientes_tab = [c for c in clientes_tab if busca.lower() in c["nome"].lower()]
    if etapa_param:
        clientes_tab = [c for c in clientes_tab if c["etapa"] == etapa_param]

    if not clientes_tab:
        st.info("Nenhum cliente encontrado.")
        st.stop()

    total = len(clientes_tab)
    st.markdown(
        f"<div style='font-size:12px;color:#8899AA;margin-bottom:10px;'>"
        f"{total} cliente(s)</div>",
        unsafe_allow_html=True,
    )

    hdr = st.columns([0.25, 3, 2, 1.8, 2.5, 0.8])
    for i, lbl in enumerate(["", "Nome", "Responsável", "Última alteração", "Última ação", ""]):
        hdr[i].markdown(
            f"<span style='font-size:11px;color:#8899AA;font-weight:700;"
            f"text-transform:uppercase;letter-spacing:.5px;'>{lbl}</span>",
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin:4px 0 6px;'>", unsafe_allow_html=True)

    por_etapa: dict = {}
    for c in clientes_tab:
        por_etapa.setdefault(c["etapa"], []).append(c)

    for etapa in ETAPAS:
        grupo = por_etapa.get(etapa, [])
        if not grupo:
            continue

        cor = COR_ETAPA.get(etapa, "#2F5AA8")
        st.markdown(
            f"""
            <div style='display:flex;align-items:center;gap:10px;padding:8px 14px;
                        background:#F8FAFB;border-radius:8px;margin:14px 0 4px;
                        border-left:4px solid {cor};'>
                <span style='font-weight:700;color:#1A2035;font-size:12px;
                             letter-spacing:.4px;'>{etapa.upper()}</span>
                <span style='background:#E5EAF2;color:#6B7A99;padding:1px 8px;
                             border-radius:10px;font-size:11px;font-weight:600;'>{len(grupo)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for c in grupo:
            cols = st.columns([0.25, 3, 2, 1.8, 2.5, 0.8])
            cols[0].markdown(
                f"<div style='width:10px;height:10px;border-radius:50%;"
                f"background:{cor};margin-top:11px;'></div>",
                unsafe_allow_html=True,
            )
            cols[1].markdown(
                f"<span style='font-weight:600;color:#1A2035;'>{c['nome']}</span><br>"
                f"<small style='color:#A0AABF;font-size:11px;'>CPF: {c.get('cpf') or '—'}</small>",
                unsafe_allow_html=True,
            )
            cols[2].write(c.get("responsavel_crm") or "—")
            cols[3].write(c.get("ultima_data") or "—")
            acao = c.get("ultima_acao", "—")
            cols[4].write(acao[:42] + "…" if len(acao) > 42 else acao)
            if cols[5].button("Ver →", key=f"lst_{c['id']}"):
                st.session_state["cliente_id_ativo"] = c["id"]
                st.switch_page("pages/2_Clientes.py")

            st.markdown(
                "<hr style='margin:2px 0;border-color:#F0F4F8;'>",
                unsafe_allow_html=True,
            )

else:
    clientes = listar_clientes(etapa=etapa_param, busca=busca or None)

    if not clientes:
        st.info("Nenhum cliente encontrado.")
        st.stop()

    st.markdown(
        f"<div style='font-size:12px;color:#8899AA;margin-bottom:16px;'>"
        f"{len(clientes)} cliente(s)</div>",
        unsafe_allow_html=True,
    )

    def _card(c: dict):
        cor     = COR_ETAPA.get(c["etapa"], "#2F5AA8")
        alerta  = ""
        validade = c.get("data_validade_credito", "")
        if validade:
            dias = (date.fromisoformat(validade) - date.today()).days
            if dias <= 30:
                alerta = f"⚠️ Crédito vence em {dias}d"

        st.markdown(
            f"""
            <div style='background:#FFFFFF;border-radius:10px;padding:14px 16px;
                        margin-bottom:10px;border-left:4px solid {cor};
                        box-shadow:0 2px 10px rgba(0,0,0,0.07);'>
                <div style='font-size:13px;font-weight:700;color:#1A2035;'>{c['nome']}</div>
                <div style='font-size:11px;color:#8899AA;margin-top:5px;'>
                    CPF: {c.get('cpf') or '—'}
                </div>
                <div style='font-size:11px;color:#8899AA;'>
                    {c.get('responsavel_crm') or '—'}
                </div>
                {f"<div style='font-size:11px;color:#E74C3C;font-weight:600;margin-top:7px;'>{alerta}</div>" if alerta else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Ver ficha →", key=f"kbn_{c['id']}"):
            st.session_state["cliente_id_ativo"] = c["id"]
            st.switch_page("pages/2_Clientes.py")

    if filtro_etapa == "Todas":
        por_etapa = {e: [] for e in ETAPAS}
        for c in clientes:
            por_etapa[c["etapa"]].append(c)

        for etapa in ETAPAS:
            grupo = por_etapa[etapa]
            if not grupo:
                continue
            cor = COR_ETAPA.get(etapa, "#2F5AA8")
            st.markdown(
                f"""
                <div style='display:flex;align-items:center;gap:10px;padding:10px 16px;
                            background:#FFFFFF;border-radius:10px;margin-bottom:10px;
                            border-left:4px solid {cor};
                            box-shadow:0 1px 6px rgba(0,0,0,0.06);'>
                    <div style='width:10px;height:10px;border-radius:50%;
                                background:{cor};flex-shrink:0;'></div>
                    <span style='font-weight:700;color:#1A2035;font-size:14px;'>{etapa}</span>
                    <span style='background:#F0F4F8;color:#6B7A99;padding:2px 9px;
                                 border-radius:10px;font-size:12px;font-weight:600;'>{len(grupo)}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            ncols = min(len(grupo), 4)
            cols  = st.columns(ncols)
            for i, c in enumerate(grupo):
                with cols[i % ncols]:
                    _card(c)
            st.markdown("")
    else:
        ncols = min(len(clientes), 4)
        cols  = st.columns(ncols)
        for i, c in enumerate(clientes):
            with cols[i % ncols]:
                _card(c)
