"""
Novo Cliente — formulário de cadastro
"""

import streamlit as st
from database import criar_cliente

st.set_page_config(page_title="Novo Cliente", page_icon="➕", layout="centered")
st.title("➕ Novo Cliente")

usuario = st.session_state.get("usuario", "Usuário")

with st.form("form_novo_cliente"):
    st.markdown("**Dados pessoais**")
    c1, c2 = st.columns(2)
    nome     = c1.text_input("Nome completo *", placeholder="João da Silva")
    cpf      = c2.text_input("CPF *", placeholder="000.000.000-00")
    telefone = c1.text_input("Telefone", placeholder="(00) 90000-0000")
    email    = c2.text_input("Email")

    st.markdown("**Imóvel / Terreno**")
    endereco = st.text_input("Endereço do imóvel / terreno")

    st.markdown("**Controle interno**")
    responsavel = st.text_input("Responsável CRM (seu nome)", value=usuario)
    obs         = st.text_area("Observações iniciais", height=80)

    submitted = st.form_submit_button("✅ Cadastrar cliente", type="primary")

if submitted:
    if not nome.strip() or not cpf.strip():
        st.error("Nome e CPF são obrigatórios.")
    else:
        try:
            cliente = criar_cliente({
                "nome": nome.strip(),
                "cpf": cpf.strip(),
                "telefone": telefone or None,
                "email": email or None,
                "endereco_imovel": endereco or None,
                "responsavel_crm": responsavel or None,
                "observacoes": obs or None,
                "etapa": "Lead",
            })
            st.success(f"✅ Cliente **{nome}** cadastrado com sucesso!")
            st.session_state["cliente_id_ativo"] = cliente["id"]
            if st.button("Ver ficha do cliente"):
                st.switch_page("pages/2_Clientes.py")
        except Exception as e:
            if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                st.error("Já existe um cliente cadastrado com esse CPF.")
            else:
                st.error(f"Erro ao cadastrar: {e}")
