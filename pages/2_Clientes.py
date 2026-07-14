"""
Clientes — lista + ficha completa com checklist de documentos e histórico
"""
import streamlit as st
from datetime import date
from database import (
    listar_clientes, buscar_cliente, atualizar_cliente, atualizar_credito,
    listar_documentos, atualizar_documento, listar_historico,
    registrar_historico, criar_checklist_engenharia,
    ETAPAS, STATUS_DOCUMENTO,
)
from utils import render_sidebar, LIGHT_CSS, COR_ETAPA

st.set_page_config(page_title="Clientes · Habitare", page_icon="👥", layout="wide")
st.markdown(LIGHT_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown(
    "<span style='font-size:22px;font-weight:700;color:#1A2035;'>👥 Clientes</span>",
    unsafe_allow_html=True,
)

usuario = st.session_state.get("usuario", "Usuário")

col_lista, col_ficha = st.columns([1, 2])

with col_lista:
    st.markdown("#### Lista")
    busca    = st.text_input("🔍 Buscar", placeholder="Nome ou CPF...")
    clientes = listar_clientes(busca=busca or None)

    if not clientes:
        st.info("Nenhum cliente.")
    else:
        for c in clientes:
            cor = COR_ETAPA.get(c["etapa"], "#2F5AA8")
            label = f"{c['nome']}  •  {c['etapa']}"
            if st.button(label, key=f"sel_{c['id']}", use_container_width=True):
                st.session_state["cliente_id_ativo"] = c["id"]

cliente_id = st.session_state.get("cliente_id_ativo")

with col_ficha:
    if not cliente_id:
        st.info("Selecione um cliente na lista ao lado.")
        st.stop()

    c = buscar_cliente(cliente_id)
    if not c:
        st.error("Cliente não encontrado.")
        st.stop()

    cor_etapa = COR_ETAPA.get(c["etapa"], "#2F5AA8")
    st.markdown(
        f"""
        <div style='margin-bottom:16px;'>
            <div style='font-size:22px;font-weight:700;color:#1A2035;'>{c['nome']}</div>
            <div style='margin-top:6px;'>
                <span style='background:{cor_etapa};color:#fff;padding:4px 12px;
                             border-radius:20px;font-size:12px;font-weight:600;'>
                    {c['etapa']}
                </span>
                <span style='font-size:12px;color:#8899AA;margin-left:12px;'>
                    CPF: {c['cpf']} · Cadastro: {c['data_cadastro'][:10]}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_dados, tab_credito, tab_docs, tab_hist = st.tabs(
        ["📋 Dados", "💳 Crédito", "📁 Documentos", "🕒 Histórico"]
    )

    with tab_dados:
        with st.form("form_dados"):
            st.markdown("**Etapa atual**")
            nova_etapa = st.selectbox("Etapa", ETAPAS, index=ETAPAS.index(c["etapa"]))

            st.markdown("**Dados pessoais**")
            c1, c2 = st.columns(2)
            nome     = c1.text_input("Nome", value=c.get("nome", ""))
            telefone = c2.text_input("Telefone", value=c.get("telefone", "") or "")
            email    = st.text_input("Email", value=c.get("email", "") or "")

            st.markdown("**Imóvel / Terreno**")
            endereco  = st.text_input("Endereço do imóvel", value=c.get("endereco_imovel", "") or "")
            c1, c2   = st.columns(2)
            matricula = c1.text_input("Nº Matrícula", value=c.get("matricula_numero", "") or "")
            cartorio  = c2.text_input("Cartório RGI",  value=c.get("cartorio_rgi", "") or "")

            st.markdown("**Responsáveis técnicos**")
            c1, c2       = st.columns(2)
            arq_nome     = c1.text_input("Arquiteto — Nome",    value=c.get("arquiteto_nome", "") or "")
            arq_contato  = c2.text_input("Arquiteto — Contato", value=c.get("arquiteto_contato", "") or "")
            rt_nome      = c1.text_input("RT — Nome",           value=c.get("responsavel_tecnico_nome", "") or "")
            rt_contato   = c2.text_input("RT — Contato",        value=c.get("responsavel_tecnico_contato", "") or "")
            rt_art       = st.text_input("Nº ART/RRT",          value=c.get("responsavel_tecnico_art", "") or "")

            st.markdown("**Conta Caixa**")
            c1, c2       = st.columns(2)
            conta_aberta = c1.checkbox("Conta aberta", value=c.get("conta_caixa_aberta", False))
            agencia      = c2.text_input("Agência", value=c.get("agencia_caixa", "") or "")

            st.markdown("**Controle interno**")
            responsavel = st.text_input("Responsável CRM", value=c.get("responsavel_crm", "") or "")
            obs         = st.text_area("Observações", value=c.get("observacoes", "") or "", height=80)

            if st.form_submit_button("💾 Salvar", type="primary"):
                atualizar_cliente(cliente_id, {
                    "etapa": nova_etapa,
                    "nome": nome,
                    "telefone": telefone,
                    "email": email,
                    "endereco_imovel": endereco,
                    "matricula_numero": matricula,
                    "cartorio_rgi": cartorio,
                    "arquiteto_nome": arq_nome,
                    "arquiteto_contato": arq_contato,
                    "responsavel_tecnico_nome": rt_nome,
                    "responsavel_tecnico_contato": rt_contato,
                    "responsavel_tecnico_art": rt_art,
                    "conta_caixa_aberta": conta_aberta,
                    "agencia_caixa": agencia,
                    "responsavel_crm": responsavel,
                    "observacoes": obs,
                }, usuario=usuario)
                st.success("Salvo!")
                st.rerun()

    with tab_credito:
        resultado = c.get("resultado_credito")
        validade  = c.get("data_validade_credito")

        if resultado is True:
            dias_restantes = (
                (date.fromisoformat(validade) - date.today()).days if validade else None
            )
            vencendo = dias_restantes is not None and dias_restantes <= 30
            cor_card  = "#FFF8E1" if vencendo else "#E8F5E9"
            cor_borda = "#F39C12" if vencendo else "#27AE60"
            st.markdown(
                f"""
                <div style='background:{cor_card};padding:16px;border-radius:10px;
                            border-left:4px solid {cor_borda};'>
                    ✅ <b>Crédito aprovado</b> em {c.get('data_analise_credito', '')}<br>
                    Válido até: <b>{validade}</b>
                    {f" — ⚠️ <b style='color:#E74C3C;'>{dias_restantes} dias restantes</b>" if vencendo else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif resultado is False:
            st.markdown(
                "<div style='background:#FFEBEE;padding:16px;border-radius:10px;"
                "border-left:4px solid #E74C3C;'>❌ <b>Crédito reprovado</b></div>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Análise de crédito ainda não registrada.")

        st.markdown("---")
        st.markdown("**Registrar / atualizar análise de crédito**")
        with st.form("form_credito"):
            c1, c2   = st.columns(2)
            data_analise = c1.date_input("Data da análise", value=date.today())
            aprovado     = c2.radio("Resultado", ["Aprovado", "Reprovado"], horizontal=True)
            if st.form_submit_button("Salvar resultado", type="primary"):
                atualizar_credito(
                    cliente_id,
                    aprovado=(aprovado == "Aprovado"),
                    data_analise=data_analise,
                    usuario=usuario,
                )
                st.success("Resultado registrado!")
                st.rerun()

    with tab_docs:
        docs = listar_documentos(cliente_id)

        if not docs:
            st.info("Nenhum documento no checklist ainda.")
            if st.button("➕ Criar checklist de Engenharia"):
                criar_checklist_engenharia(cliente_id)
                registrar_historico(cliente_id, usuario, "Checklist de Engenharia criado manualmente")
                st.rerun()
        else:
            fases = {}
            for d in docs:
                fases.setdefault(d["fase"], []).append(d)

            BADGE = {"Pendente": "🔴", "Enviado": "🔵", "Aprovado": "🟢", "Rejeitado": "⛔"}

            for fase, itens in fases.items():
                aprovados = sum(1 for i in itens if i["status"] == "Aprovado")
                st.markdown(f"**{fase}** — {aprovados}/{len(itens)} aprovados")

                for doc in itens:
                    with st.expander(f"{BADGE.get(doc['status'], '•')} {doc['tipo']}  —  {doc['status']}"):
                        with st.form(f"doc_{doc['id']}"):
                            novo_status = st.selectbox(
                                "Status", STATUS_DOCUMENTO,
                                index=STATUS_DOCUMENTO.index(doc["status"]),
                                key=f"st_{doc['id']}",
                            )
                            obs_doc = st.text_input(
                                "Observação", value=doc.get("observacoes", "") or "",
                                key=f"obs_{doc['id']}",
                            )
                            if st.form_submit_button("Atualizar"):
                                atualizar_documento(doc["id"], novo_status, usuario, obs_doc)
                                if novo_status != doc["status"]:
                                    registrar_historico(
                                        cliente_id, usuario,
                                        f"Documento '{doc['tipo']}': {doc['status']} → {novo_status}",
                                    )
                                st.rerun()

    with tab_hist:
        historico = listar_historico(cliente_id)
        if not historico:
            st.info("Sem histórico.")
        else:
            for h in historico:
                data_str = h["data"][:16].replace("T", " ")
                st.markdown(
                    f"**{data_str}** — {h['usuario']}  \n{h['acao']}"
                    + (f"\n\n*{h['detalhe']}*" if h.get("detalhe") else "")
                )
                st.markdown("---")

        st.markdown("**Adicionar nota manual**")
        with st.form("form_nota"):
            nota = st.text_area("Nota", height=80)
            if st.form_submit_button("Registrar nota", type="primary"):
                if nota.strip():
                    registrar_historico(cliente_id, usuario, "Nota", nota)
                    st.rerun()
