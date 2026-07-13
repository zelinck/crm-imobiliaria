"""
database.py — Camada de dados: Supabase + todas as queries do Módulo 1
"""

import os
from datetime import date, timedelta
from typing import Optional
from supabase import create_client, Client
import streamlit as st

# =============================================================
# CONEXÃO
# =============================================================

ETAPAS = [
    "Lead",
    "Análise de Crédito",
    "Crédito Reprovado",
    "Crédito Aprovado",
    "Abertura de Conta",
    "Documentação Engenharia",
    "SIOP",
    "Assinatura Digital",
    "Análise Digital",
    "Assinatura Contrato",
    "Cartório",
    "Concluído",
]

ETAPAS_ATIVAS = [e for e in ETAPAS if e not in ("Crédito Reprovado", "Concluído")]

DOCUMENTOS_ENGENHARIA = [
    "Certidão de Matrícula",
    "Projeto Legal (aprovado Prefeitura)",
    "ART/RRT/TRT do Projeto",
    "ART/RRT/TRT da Execução",
    "Alvará de Construção",
    "PCI - Proposta de Construção Individual",
    "Memorial Descritivo",
    "Orçamento da Obra (PLS)",
    "Cronograma de Obra",
    "CNO - Cadastro Nacional de Obras",
    "SCPO - Comunicação Prévia de Obra",
    "Poligonal do Terreno",
]

STATUS_DOCUMENTO = ["Pendente", "Enviado", "Aprovado", "Rejeitado"]


@st.cache_resource
def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def db() -> Client:
    return get_client()


# =============================================================
# CLIENTES
# =============================================================

def listar_clientes(etapa: Optional[str] = None, busca: Optional[str] = None):
    q = db().table("clientes").select("*").order("data_cadastro", desc=True)
    if etapa:
        q = q.eq("etapa", etapa)
    if busca:
        q = q.ilike("nome", f"%{busca}%")
    return q.execute().data


def buscar_cliente(cliente_id: str):
    res = db().table("clientes").select("*").eq("id", cliente_id).single().execute()
    return res.data


def criar_cliente(dados: dict) -> dict:
    res = db().table("clientes").insert(dados).execute()
    cliente = res.data[0]
    registrar_historico(cliente["id"], "Sistema", "Cliente cadastrado")
    return cliente


def atualizar_cliente(cliente_id: str, dados: dict, usuario: str = "Sistema"):
    atual = buscar_cliente(cliente_id)
    etapa_anterior = atual.get("etapa")

    res = db().table("clientes").update(dados).eq("id", cliente_id).execute()

    if "etapa" in dados and dados["etapa"] != etapa_anterior:
        registrar_historico(
            cliente_id,
            usuario,
            f"Etapa alterada: {etapa_anterior} → {dados['etapa']}"
        )
        if dados["etapa"] == "Crédito Aprovado":
            criar_checklist_engenharia(cliente_id)

    return res.data[0] if res.data else None


def atualizar_credito(cliente_id: str, aprovado: bool, data_analise: date, usuario: str = "Sistema"):
    validade = data_analise + timedelta(days=180)
    nova_etapa = "Crédito Aprovado" if aprovado else "Crédito Reprovado"
    dados = {
        "resultado_credito": aprovado,
        "data_analise_credito": data_analise.isoformat(),
        "data_validade_credito": validade.isoformat(),
        "etapa": nova_etapa,
    }
    return atualizar_cliente(cliente_id, dados, usuario)


# =============================================================
# DOCUMENTOS
# =============================================================

def criar_checklist_engenharia(cliente_id: str):
    existentes = db().table("documentos").select("tipo").eq("cliente_id", cliente_id).execute().data
    tipos_existentes = {d["tipo"] for d in existentes}

    novos = [
        {"cliente_id": cliente_id, "tipo": doc, "fase": "Engenharia"}
        for doc in DOCUMENTOS_ENGENHARIA
        if doc not in tipos_existentes
    ]
    if novos:
        db().table("documentos").insert(novos).execute()


def listar_documentos(cliente_id: str):
    return (
        db().table("documentos")
        .select("*")
        .eq("cliente_id", cliente_id)
        .order("fase")
        .order("tipo")
        .execute()
        .data
    )


def atualizar_documento(doc_id: str, status: str, usuario: str, observacoes: str = ""):
    hoje = date.today().isoformat()
    dados = {
        "status": status,
        "atualizado_por": usuario,
        "data_atualizacao": "now()",
        "observacoes": observacoes,
    }
    if status == "Enviado":
        dados["data_envio"] = hoje
    elif status == "Aprovado":
        dados["data_aprovacao"] = hoje

    db().table("documentos").update(dados).eq("id", doc_id).execute()


# =============================================================
# HISTÓRICO
# =============================================================

def registrar_historico(cliente_id: str, usuario: str, acao: str, detalhe: str = ""):
    db().table("historico").insert({
        "cliente_id": cliente_id,
        "usuario": usuario,
        "acao": acao,
        "detalhe": detalhe,
    }).execute()


def listar_historico(cliente_id: str):
    return (
        db().table("historico")
        .select("*")
        .eq("cliente_id", cliente_id)
        .order("data", desc=True)
        .execute()
        .data
    )


# =============================================================
# PIPELINE / DASHBOARD
# =============================================================

def contar_por_etapa() -> dict:
    res = db().table("clientes").select("etapa").execute().data
    contagem = {e: 0 for e in ETAPAS}
    for row in res:
        etapa = row["etapa"]
        if etapa in contagem:
            contagem[etapa] += 1
    return contagem


def alertas_credito_vencendo(dias: int = 30):
    hoje = date.today()
    limite = hoje + timedelta(days=dias)
    return (
        db().table("clientes")
        .select("id, nome, etapa, data_validade_credito, responsavel_crm")
        .gte("data_validade_credito", hoje.isoformat())
        .lte("data_validade_credito", limite.isoformat())
        .not_.in_("etapa", ["Concluído", "Crédito Reprovado"])
        .order("data_validade_credito")
        .execute()
        .data
    )


def alertas_documentos_pendentes(dias: int = 15):
    limite = (date.today() - timedelta(days=dias)).isoformat()
    return (
        db().table("documentos")
        .select("id, tipo, fase, cliente_id, clientes(nome, etapa)")
        .eq("status", "Pendente")
        .lte("data_atualizacao", limite)
        .execute()
        .data
    )
