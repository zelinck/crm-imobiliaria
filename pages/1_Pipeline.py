"""
Pipeline — visão geral do funil por etapa, com cards clicáveis por cliente
"""

import streamlit as st
from datetime import date
from database import listar_clientes, ETAPAS

st.set_page_config(page_title="Pipeline", page_icon="📋", layout="wide")
st.title("📋 Pipeline de Financiamento")

# Filtros
col_busca, col_etapa, _ = st.columns([2, 2, 3])
busca = col_busca.text_input("🔍 Buscar cliente", placeholder="Nome...")
filtro_etapa = col_etapa.selectbox("Filtrar etapa", ["Todas"] + ETAPAS)

COR_ETAPA = {
    "Lead": "#e9ecef",
    "Análise de Crédito": "#fff3cd",
    "Crédito Reprovado": "#f8d7da",
    "Crédito Aprovado": "#d1e7dd",
    "Abertura de Conta": "#cfe2ff",
    "Documentação Engenharia": "#d0d5fb",
    "SIOP": "#e2d9f3",
    "Assinatura Digital": "#fde68a",
    "Análise Digital": "#fed7aa",
    "Assinatura Contrato": "#bbf7d0",
    "Cartório": "#a7f3d0",
    "Concluído": "#6ee7b7",
}

def _card_cliente(c: dict):
    cor = COR_ETAPA.get(c["etapa"], "#f8f9fa")
    validade = c.get("data_validade_credito", "")
    alerta_credito = ""
    if validade:
        dias = (date.fromisoformat(validade) - date.today()).days
        if dias <= 30:
            alerta_credito = f"⚠️ Crédito vence em {dias}d"

    with st.container():
        st.markdown(
            f"""
            <div style='background:{cor};border-radius:10px;padding:12px 14px;
                        margin-bottom:10px;border:1px solid #dee2e6;'>
                <b>{c['nome']}</b><br>
                <small>CPF: {c.get('cpf') or '—'}</small><br>
                <small>{c.get('responsavel_crm','') or ''}</small><br>
                {f"<small style='color:#dc3545;'>{alerta_credito}</small>" if alerta_credito else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Ver ficha", key=f"btn_{c['id']}"):
            st.session_state["cliente_id_ativo"] = c["id"]
            st.switch_page("pages/2_Clientes.py")

# Busca
etapa_param = None if filtro_etapa == "Todas" else filtro_etapa
clientes = listar_clientes(etapa=etapa_param, busca=busca or None)

st.markdown(f"**{len(clientes)} cliente(s) encontrado(s)**")
st.markdown("---")

if not clientes:
    st.info("Nenhum cliente encontrado.")
    st.stop()

# Renderiza
if filtro_etapa == "Todas":
    por_etapa = {e: [] for e in ETAPAS}
    for c in clientes:
        por_etapa[c["etapa"]].append(c)

    for etapa in ETAPAS:
        grupo = por_etapa[etapa]
        if not grupo:
            continue
        cor = COR_ETAPA.get(etapa, "#f8f9fa")
        st.markdown(
            f"<h4 style='background:{cor};padding:8px 14px;border-radius:8px;'>"
            f"{etapa} <span style='font-size:14px;font-weight:400;'>({len(grupo)})</span></h4>",
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
