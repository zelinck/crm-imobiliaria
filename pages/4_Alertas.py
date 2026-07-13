"""
Alertas — créditos vencendo + documentos pendentes
"""

import streamlit as st
from datetime import date
from database import alertas_credito_vencendo, alertas_documentos_pendentes

st.set_page_config(page_title="Alertas", page_icon="⚠️", layout="wide")
st.title("⚠️ Alertas")
st.caption(f"Atualizado em {date.today().strftime('%d/%m/%Y')}")

# ----------------------------------------------------------
# CRÉDITOS VENCENDO
# ----------------------------------------------------------
st.markdown("### 💳 Análises de crédito vencendo em 30 dias")

vencendo = alertas_credito_vencendo(30)

if not vencendo:
    st.success("Nenhuma análise vencendo nos próximos 30 dias. ✅")
else:
    for c in vencendo:
        validade   = date.fromisoformat(c["data_validade_credito"])
        dias_rest  = (validade - date.today()).days
        cor        = "#f8d7da" if dias_rest <= 15 else "#fff3cd"
        urgencia   = "🔴 URGENTE" if dias_rest <= 15 else "🟡 Atenção"

        st.markdown(
            f"<div style='background:{cor};padding:12px 16px;border-radius:8px;margin-bottom:8px;'>"
            f"<b>{urgencia}</b> — <b>{c['nome']}</b><br>"
            f"Etapa: {c['etapa']}  •  "
            f"Responsável: {c.get('responsavel_crm') or '—'}  •  "
            f"Vence: <b>{validade.strftime('%d/%m/%Y')}</b> ({dias_rest} dias)"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("Abrir ficha", key=f"alc_{c['id']}"):
            st.session_state["cliente_id_ativo"] = c["id"]
            st.switch_page("pages/2_Clientes.py")

st.markdown("---")

# ----------------------------------------------------------
# DOCUMENTOS PENDENTES HÁ MAIS DE 15 DIAS
# ----------------------------------------------------------
st.markdown("### 📁 Documentos pendentes há mais de 15 dias")

pendentes = alertas_documentos_pendentes(15)

if not pendentes:
    st.success("Nenhum documento pendente antigo. ✅")
else:
    # Agrupa por cliente
    por_cliente = {}
    for d in pendentes:
        nome_cliente = d.get("clientes", {}).get("nome", "Desconhecido") if isinstance(d.get("clientes"), dict) else "—"
        cid = d["cliente_id"]
        por_cliente.setdefault(cid, {"nome": nome_cliente, "docs": []})
        por_cliente[cid]["docs"].append(d["tipo"])

    for cid, info in por_cliente.items():
        st.markdown(
            f"<div style='background:#fff3cd;padding:12px 16px;border-radius:8px;margin-bottom:8px;'>"
            f"<b>{info['nome']}</b> — {len(info['docs'])} doc(s) pendente(s):<br>"
            f"<small>{'  •  '.join(info['docs'])}</small>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("Abrir ficha", key=f"ald_{cid}"):
            st.session_state["cliente_id_ativo"] = cid
            st.switch_page("pages/2_Clientes.py")
