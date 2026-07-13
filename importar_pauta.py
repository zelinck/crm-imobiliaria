"""
importar_pauta.py — Importa dados da planilha PAUTA para o Supabase.
Rode UMA VEZ: python importar_pauta.py

Mapeamento de Status Excel -> Etapa CRM:
"""

import openpyxl
from supabase import create_client

SUPABASE_URL = "https://scoebqhbpkmnhbdchnpc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNjb2VicWhicGttbmhiZGNobnBjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM5NzM2MzAsImV4cCI6MjA5OTU0OTYzMH0.cJXkf4eMfdYxcvYG8gYz0gVlW-ZK0KF9s9__bwTyCbk"

def mapear_etapa(status: str) -> str:
    if not status:
        return "Lead"
    s = status.lower().strip()

    if any(x in s for x in ["registr", "cartorio", "cartorio", "prenotado", "nota final"]):
        return "Cartorio"
    if any(x in s for x in ["finalizou o registro", "liberou o recurso"]):
        return "Concluido"
    if any(x in s for x in ["assinou o contrato", "assinou hj", "assinou contrato"]):
        return "Assinatura Contrato"
    if any(x in s for x in ["tiramos a nota", "tirou nota", "pedir nota"]):
        return "SIOP"
    if any(x in s for x in ["conformidade", "conforme", "na conformidade"]):
        return "Analise Digital"
    if any(x in s for x in ["inconforme", "falta atualizar", "falta certidao"]):
        return "Documentacao Engenharia"
    if any(x in s for x in ["montando pasta", "montando", "pedir engenharia"]):
        return "Documentacao Engenharia"
    if any(x in s for x in ["entrevista", "liberou o recurso do terreno"]):
        return "Abertura de Conta"
    if any(x in s for x in ["relacionamento", "aguardando demanda", "sem reserva"]):
        return "Lead"
    if any(x in s for x in ["gerar contrato", "contrato de obra"]):
        return "Assinatura Digital"
    return "Lead"

def main():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    wb = openpyxl.load_workbook("PAUTA 10.07.26.xlsx")
    ws = wb["Vendas Imoveis"]

    inseridos = 0
    erros = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        nome, cpf, imovel, status, obs, corretor = row

        if not nome or str(nome).strip().lower() in ("cliente", ""):
            continue

        nome = str(nome).strip()
        cpf_str = str(cpf).strip() if cpf else None
        imovel_str = str(imovel).strip() if imovel else None
        obs_str = str(obs).strip() if obs else None
        corretor_str = str(corretor).strip() if corretor else None
        etapa = mapear_etapa(status)

        obs_final = ""
        if status:
            obs_final += f"[Pauta] Status original: {status}"
        if obs_str:
            obs_final += f" | Obs: {obs_str}"
        if corretor_str:
            obs_final += f" | Corretor: {corretor_str}"

        registro = {
            "nome": nome,
            "cpf": cpf_str,
            "endereco_imovel": imovel_str,
            "etapa": etapa,
            "responsavel_crm": corretor_str,
            "observacoes": obs_final.strip(" |"),
        }

        try:
            supabase.table("clientes").insert(registro).execute()
            print(f"OK {nome} -> {etapa}")
            inseridos += 1
        except Exception as e:
            err = str(e)
            if "duplicate" in err.lower() or "unique" in err.lower():
                print(f"AVISO {nome} - CPF duplicado, pulando")
            else:
                print(f"ERRO {nome}: {err}")
                erros.append(nome)

    print(f"\n{'='*50}")
    print(f"Importados: {inseridos} clientes")
    if erros:
        print(f"Erros: {erros}")

if __name__ == "__main__":
    main()
