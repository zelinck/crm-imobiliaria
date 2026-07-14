"""
Alertas — créditos vencendo + documentos pendentes
"""
import streamlit as st
from datetime import date
from database import alertas_credito_vencendo, alertas_documentos_pendentes
from utils import render_sidebar, LIGHT_CSS

st.set_page_config(page_title="Alertas · Habitare", page_icon="⚠️", layout="wide")
st.markdown(LIGHT_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown(
    "<span style='font-size:22px;font-weight:700;color:#1A2035;'>⚠️ Alertas</span>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<div style='color:#8899AA;font-size:13px;margin-bottom:20px;'>"
    f"Atualizado em {date.today().strftime('%d/%m/%Y')}</div>",
    unsafe_allow_html=True,
)

# ── Créditos vencendo ──────────────────────────────────────────
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#1A2035;margin-bottom:12px;'>"
    "💳 Análises de crédito vencendo em 30 dias</div>",
    unsafe_allow_html=True,
)

vencendo = alertas_credito_vencendo(30)

if not vencendo:
    st.success("Nenhuma análise vencendo nos próximos 30 dias. ✅")
else:
    for c in vencendo:
        validade  = date.fromisoformat(c["data_validade_credito"])
        dias_rest = (validade - date.today()).days
        urgente   = dias_rest <= 15
        cor       = "#FFEBEE" if urgente else "#FFF8E1"
        borda     = "#E74C3C" if urgente else "#F39C12"
        tag       = "🔴 URGENTE" if urgente else "🟡 Atenção"

        st.markdown(
            f"""
            <div style='background:{cor};padding:14px 18px;border-radius:10px;
                        border-left:4px solid {borda};margin-bottom:10px;'>
                <b>{tag}</b> — <b>{c['nome']}</b><br>
                <span style='font-size:13px;color:#5A6A8A;'>
                    Etapa: {c['etapa']}  ·
                    Responsável: {c.get('responsavel_crm') or '—'}  ·
                    Vence: <b>{validade.strftime('%d/%m/%Y')}</b> ({dias_rest} dias)
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Abrir ficha →", key=f"alc_{c['id']}"):
            st.session_state["cliente_id_ativo"] = c["id"]
            st.switch_page("pages/2_Clientes.py")

st.markdown("<hr style='margin:24px 0;'>", unsafe_allow_html=True)

# ── Documentos pendentes ───────────────────────────────────────
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#1A2035;margin-bottom:12px;'>"
    "📁 Documentos pendentes há mais de 15 dias</div>",
    unsafe_allow_html=True,
)

pendentes = alertas_documentos_pendentes(15)

if not pendentes:
    st.success("Nenhum documento pendente antigo. ✅")
else:
    por_cliente: dict = {}
    for d in pendentes:
        nome_cliente = (
            d.get("clientes", {}).get("nome", "Desconhecido")
            if isinstance(d.get("clientes"), dict)
            else "—"
        )
        cid = d["cliente_id"]
        por_cliente.setdefault(cid, {"nome": nome_cliente, "docs": []})
        por_cliente[cid]["docs"].append(d["tipo"])

    for cid, info in por_cliente.items():
        st.markdown(
            f"""
            <div style='background:#FFF8E1;padding:14px 18px;border-radius:10px;
                        border-left:4px solid #F39C12;margin-bottom:10px;'>
                <b>{info['nome']}</b> — {len(info['docs'])} documento(s) pendente(s):<br>
                <span style='font-size:12px;color:#5A6A8A;'>
                    {'  ·  '.join(info['docs'])}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Abrir ficha →", key=f"ald_{cid}"):
            st.session_state["cliente_id_ativo"] = cid
            st.switch_page("pages/2_Clientes.py")
