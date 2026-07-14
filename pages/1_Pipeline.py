"""
Pipeline — visão Kanban e Lista do funil de financiamento
"""

import streamlit as st
from datetime import date
from database import listar_clientes, listar_clientes_tabela, ETAPAS

st.set_page_config(page_title="Pipeline", page_icon="📋", layout="wide")
st.title("📋 Pipeline de Financiamento")

# ── Habitare color palette ──────────────────────────────────────
HAB_PRIMARY  = "#2F5AA8"
HAB_DARK     = "#0e2144"
HAB_LIGHT    = "#b8d4f5"

COR_ETAPA = {
    "Lead":                    "#dce8f5",
    "Análise de Crédito":      "#fff0b3",
    "Crédito Reprovado":       "#fad3d7",
    "Crédito Aprovado":        "#c8ead8",
    "Abertura de Conta":       "#b8d4f5",
    "Documentação Engenharia": "#d4d9ff",
    "SIOP":                    "#e4d4f5",
    "Assinatura Digital":      "#fde68a",
    "Análise Digital":         "#fdd5a8",
    "Assinatura Contrato":     "#b3f0cc",
    "Cartório":                "#90e8c0",
    "Concluído":               "#5de0a8",
}

TEXTO_ETAPA = {
    "Lead":                    "#0d2d5a",
    "Análise de Crédito":      "#5c4a00",
    "Crédito Reprovado":       "#7a0c17",
    "Crédito Aprovado":        "#0a3622",
    "Abertura de Conta":       "#0d2d5a",
    "Documentação Engenharia": "#1a1f6e",
    "SIOP":                    "#3d0f6e",
    "Assinatura Digital":      "#5c4a00",
    "Análise Digital":         "#6b3200",
    "Assinatura Contrato":     "#0a3622",
    "Cartório":                "#0a3622",
    "Concluído":               "#0a3622",
}

# ── Filtros ─────────────────────────────────────────────────────
col_busca, col_etapa, col_view, _ = st.columns([2, 2, 2, 1])
busca        = col_busca.text_input("🔍 Buscar cliente", placeholder="Nome...")
filtro_etapa = col_etapa.selectbox("Filtrar etapa", ["Todas"] + ETAPAS)
modo         = col_view.radio("Visualização", ["📋 Kanban", "📊 Lista"], horizontal=True)

etapa_param = None if filtro_etapa == "Todas" else filtro_etapa

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# VISÃO KANBAN
# ══════════════════════════════════════════════════════════════
if modo == "📋 Kanban":
    clientes = listar_clientes(etapa=etapa_param, busca=busca or None)
    st.markdown(f"**{len(clientes)} cliente(s) encontrado(s)**")

    if not clientes:
        st.info("Nenhum cliente encontrado.")
        st.stop()

    def _card_cliente(c: dict):
        cor_bg   = COR_ETAPA.get(c["etapa"], "#dce8f5")
        cor_txt  = TEXTO_ETAPA.get(c["etapa"], "#0d2d5a")
        alerta_credito = ""
        validade = c.get("data_validade_credito", "")
        if validade:
            dias = (date.fromisoformat(validade) - date.today()).days
            if dias <= 30:
                alerta_credito = f"⚠️ Crédito vence em {dias}d"

        with st.container():
            st.markdown(
                f"""
                <div style='background:{cor_bg};border-radius:10px;padding:12px 14px;
                            margin-bottom:10px;border-left:4px solid {HAB_PRIMARY};color:{cor_txt};'>
                    <b style='font-size:14px;'>{c['nome']}</b><br>
                    <small>CPF: {c.get('cpf') or '—'}</small><br>
                    <small>{c.get('responsavel_crm','') or ''}</small>
                    {f"<br><small style='color:#c0392b;font-weight:600;'>{alerta_credito}</small>" if alerta_credito else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Ver ficha", key=f"btn_{c['id']}"):
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
            cor_bg  = COR_ETAPA.get(etapa, "#dce8f5")
            cor_txt = TEXTO_ETAPA.get(etapa, "#0d2d5a")
            st.markdown(
                f"<h4 style='background:{cor_bg};color:{cor_txt};padding:8px 16px;"
                f"border-radius:8px;border-left:4px solid {HAB_PRIMARY};'>"
                f"{etapa} <span style='font-size:13px;font-weight:400;'>({len(grupo)})</span></h4>",
                unsafe_allow_html=True,
            )
            cols = st.columns(min(len(grupo), 4))
            for i, c in enumerate(grupo):
                with cols[i % 4]:
                    _card_cliente(c)
            st.markdown("")
    else:
        cols = st.columns(min(len(clientes), 4))
        for i, c in enumerate(clientes):
            with cols[i % 4]:
                _card_cliente(c)

# ══════════════════════════════════════════════════════════════
# VISÃO LISTA / TABULAR
# ══════════════════════════════════════════════════════════════
else:
    clientes_tab = listar_clientes_tabela()

    if busca:
        clientes_tab = [c for c in clientes_tab if busca.lower() in c["nome"].lower()]
    if etapa_param:
        clientes_tab = [c for c in clientes_tab if c["etapa"] == etapa_param]

    st.markdown(f"**{len(clientes_tab)} cliente(s) encontrado(s)**")

    if not clientes_tab:
        st.info("Nenhum cliente encontrado.")
        st.stop()

    # Cabeçalho
    hdr = st.columns([3, 2, 2, 2, 2, 1])
    hdr[0].markdown(f"<b style='color:{HAB_LIGHT};'>Cliente</b>", unsafe_allow_html=True)
    hdr[1].markdown(f"<b style='color:{HAB_LIGHT};'>Etapa</b>", unsafe_allow_html=True)
    hdr[2].markdown(f"<b style='color:{HAB_LIGHT};'>Responsável</b>", unsafe_allow_html=True)
    hdr[3].markdown(f"<b style='color:{HAB_LIGHT};'>Última alteração</b>", unsafe_allow_html=True)
    hdr[4].markdown(f"<b style='color:{HAB_LIGHT};'>Última ação</b>", unsafe_allow_html=True)
    hdr[5].markdown("")

    st.markdown(
        f"<hr style='border:none;border-top:2px solid {HAB_PRIMARY};margin:4px 0 8px 0;'/>",
        unsafe_allow_html=True
    )

    for c in clientes_tab:
        cor_bg  = COR_ETAPA.get(c["etapa"], "#dce8f5")
        cor_txt = TEXTO_ETAPA.get(c["etapa"], "#0d2d5a")

        row = st.columns([3, 2, 2, 2, 2, 1])
        row[0].markdown(f"**{c['nome']}**  \n<small style='color:#8899bb;'>CPF: {c.get('cpf') or '—'}</small>", unsafe_allow_html=True)
        row[1].markdown(
            f"<span style='background:{cor_bg};color:{cor_txt};padding:3px 9px;"
            f"border-radius:10px;font-size:12px;font-weight:600;'>{c['etapa']}</span>",
            unsafe_allow_html=True
        )
        row[2].write(c.get("responsavel_crm") or "—")
        row[3].write(c.get("ultima_data") or "—")
        acao = c.get("ultima_acao", "—")
        row[4].write(acao[:45] + "…" if len(acao) > 45 else acao)

        if row[5].button("Ver", key=f"lst_{c['id']}"):
            st.session_state["cliente_id_ativo"] = c["id"]
            st.switch_page("pages/2_Clientes.py")

        st.markdown(
            f"<hr style='border:none;border-top:1px solid #1e3060;margin:2px 0;'/>",
            unsafe_allow_html=True
        )
