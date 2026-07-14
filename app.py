"""
app.py — Dashboard principal · CRM Habitare MCMV
"""
import streamlit as st

st.set_page_config(
    page_title="CRM Habitare",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils import render_sidebar, LIGHT_CSS, LOGO_URL, COR_ETAPA

st.markdown(LIGHT_CSS, unsafe_allow_html=True)
render_sidebar()

# ── Cabeçalho ──────────────────────────────────────────────
col_logo, col_title = st.columns([0.7, 5])
with col_logo:
    try:
        st.image(LOGO_URL, width=68)
    except Exception:
        st.markdown("🏠")
with col_title:
    st.markdown(
        """
        <div style='padding-top:8px;'>
            <div style='font-size:24px;font-weight:700;color:#1A2035;line-height:1.1;'>
                Habitare Imobiliária
            </div>
            <div style='font-size:13px;color:#6B7A99;margin-top:4px;'>
                CRM · Correspondente Caixa Econômica Federal · Financiamento MCMV
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='margin:18px 0 24px;'>", unsafe_allow_html=True)

# ── Dados ──────────────────────────────────────────────────────
try:
    from database import (
        contar_por_etapa, alertas_credito_vencendo,
        listar_clientes, ETAPAS_ATIVAS, ETAPAS,
    )

    contagem     = contar_por_etapa()
    total_ativos = sum(v for k, v in contagem.items() if k in ETAPAS_ATIVAS)
    concluidos   = contagem.get("Concluído", 0)
    reprovados   = contagem.get("Crédito Reprovado", 0)
    alertas_n    = len(alertas_credito_vencendo(30))

    kpis = [
        (total_ativos, "Clientes ativos",          "#2F5AA8"),
        (concluidos,   "Financiamentos concluídos", "#27AE60"),
        (reprovados,   "Créditos reprovados",       "#E74C3C"),
        (alertas_n,    "Alertas de crédito",        "#F39C12"),
    ]
    kpi_cols = st.columns(4)
    for i, (val, label, cor) in enumerate(kpis):
        kpi_cols[i].markdown(
            f"""
            <div style='background:#fff;border-radius:14px;padding:22px 24px;
                        box-shadow:0 2px 10px rgba(0,0,0,0.07);border-top:4px solid {cor};'>
                <div style='font-size:11px;color:#8899AA;font-weight:700;
                            text-transform:uppercase;letter-spacing:.6px;'>{label}</div>
                <div style='font-size:36px;font-weight:800;color:{cor};margin-top:8px;
                            line-height:1;'>{val}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='font-size:17px;font-weight:700;color:#1A2035;margin-bottom:2px;'>
            Distribuição por etapa
        </div>
        <div style='font-size:13px;color:#8899AA;margin-bottom:18px;'>
            Clique em uma etapa para ver os clientes
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "etapa_selecionada" not in st.session_state:
        st.session_state["etapa_selecionada"] = None

    ETAPAS_SHOW = [e for e in ETAPAS if e != "Crédito Reprovado"]
    COLS_PER_ROW = 5

    for row_start in range(0, len(ETAPAS_SHOW), COLS_PER_ROW):
        chunk = ETAPAS_SHOW[row_start : row_start + COLS_PER_ROW]
        ccols = st.columns(COLS_PER_ROW)

        for j, etapa in enumerate(chunk):
            n         = contagem.get(etapa, 0)
            selecion  = st.session_state["etapa_selecionada"] == etapa
            cor       = COR_ETAPA.get(etapa, "#2F5AA8")
            bg        = "#EDF3FF" if selecion else "#FFFFFF"
            border    = f"2px solid {cor}" if selecion else "2px solid #E8EEF6"
            shadow    = f"0 4px 14px {cor}33" if selecion else "0 2px 8px rgba(0,0,0,0.06)"

            with ccols[j]:
                st.markdown(
                    f"""
                    <div style='background:{bg};border-radius:12px;padding:16px 10px 10px;
                                border:{border};box-shadow:{shadow};text-align:center;
                                margin-bottom:4px;'>
                        <div style='font-size:28px;font-weight:800;color:{cor};'>{n}</div>
                        <div style='font-size:11px;color:#6B7A99;margin-top:4px;
                                    line-height:1.3;'>{etapa}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                btn_lbl = "✓ Selecionado" if selecion else "Ver clientes"
                if st.button(
                    btn_lbl,
                    key=f"card_{etapa}",
                    use_container_width=True,
                    type="primary" if selecion else "secondary",
                ):
                    st.session_state["etapa_selecionada"] = (
                        None if selecion else etapa
                    )
                    st.rerun()

    etapa_sel = st.session_state.get("etapa_selecionada")
    if etapa_sel:
        cor_sel = COR_ETAPA.get(etapa_sel, "#2F5AA8")
        st.markdown(
            f"""
            <div style='margin:28px 0 14px;display:flex;align-items:center;gap:10px;'>
                <div style='width:12px;height:12px;border-radius:50%;
                            background:{cor_sel};flex-shrink:0;'></div>
                <span style='font-size:17px;font-weight:700;color:#1A2035;'>
                    Clientes em: {etapa_sel}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        clientes = listar_clientes(etapa=etapa_sel)
        if not clientes:
            st.info("Nenhum cliente nesta etapa.")
        else:
            hcols = st.columns([3, 2, 2, 1])
            for i, lbl in enumerate(["Cliente", "Responsável", "Cadastro", ""]):
                hcols[i].markdown(
                    f"<span style='font-size:11px;color:#8899AA;font-weight:700;"
                    f"text-transform:uppercase;letter-spacing:.5px;'>{lbl}</span>",
                    unsafe_allow_html=True,
                )
            st.markdown("<hr style='margin:4px 0 8px;'>", unsafe_allow_html=True)

            for c in clientes:
                row = st.columns([3, 2, 2, 1])
                row[0].markdown(
                    f"<span style='font-weight:600;color:#1A2035;'>{c['nome']}</span><br>"
                    f"<small style='color:#8899AA;'>CPF: {c.get('cpf') or '—'}</small>",
                    unsafe_allow_html=True,
                )
                row[1].write(c.get("responsavel_crm") or "—")
                row[2].write((c.get("data_cadastro") or "")[:10])
                if row[3].button("Ver →", key=f"home_ver_{c['id']}"):
                    st.session_state["cliente_id_ativo"] = c["id"]
                    st.switch_page("pages/2_Clientes.py")
                st.markdown(
                    "<hr style='margin:2px 0;border-color:#F0F4F8;'>",
                    unsafe_allow_html=True,
                )

except Exception as e:
    st.info(
        "Configure as credenciais do Supabase em `.streamlit/secrets.toml` para começar."
    )
    st.caption(f"Detalhe: {e}")
