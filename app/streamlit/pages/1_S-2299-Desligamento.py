
import streamlit as st
import pandas as pd

from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento

from app.etl.extract.desligamento import extract
from app.etl.load.desligamento import load
from app.etl.transform.desligamento import transformar_desligamento
from lxml import etree

from app.services.processamento_desligamento import (
    processar_eventos,
)


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="eSocial",
    page_icon="📋",
    layout="wide"
)

st.title("📋 eSocial - S-2299 - Desligamentos")


# ==========================================================
# CARGA DOS DESLIGAMENTOS
# ==========================================================

st.subheader("📥 Carga de desligamentos")

if st.button(
    "🚀 Carregar desligamentos",
    type="primary"
):

    try:

        with st.spinner("Extraindo dados do banco de origem..."):

            df = extract()
            load(df)

        with st.spinner("Transformando desligamentos..."):

            with SessionLocal() as session:

                eventos = transformar_desligamento(session)

                session.add_all(eventos)
                session.commit()

                qtd_eventos = (
                    session.query(EsocialDesligamento).count()
                )

        st.success("Carga concluída com sucesso!")

        st.info(
            f"{qtd_eventos} desligamentos cadastrados no banco local."
        )

    except Exception as e:

        st.error(f"Erro durante a carga: {e}")


# ==========================================================
# CONSULTA DOS REGISTROS
# ==========================================================

st.divider()

st.subheader("📊 Registros de desligamentos")

with SessionLocal() as session:

    total_registros = (
        session.query(EsocialDesligamento).count()
    )

    total_com_id = (
        session.query(EsocialDesligamento)
        .filter(EsocialDesligamento.id_evento.is_not(None))
        .count()
    )

    total_com_xml = (
        session.query(EsocialDesligamento)
        .filter(
            EsocialDesligamento.xml.is_not(None),
            EsocialDesligamento.xml != ""
        )
        .count()
    )

    dados = [
        {
            "id": registro.id,
            "matricula": registro.matricula,
            "cpf_trab": registro.cpf_trab,
            "dt_deslig": registro.dt_deslig,
            "mtv_deslig": registro.mtv_deslig,
            "ind_pagto_api": registro.ind_pagto_api,
            "tipo_evento": registro.tipo_evento,
            "status": registro.status,
            "id_evento": registro.id_evento,
            "protocolo_envio": registro.protocolo_envio,
            "recibo": registro.recibo,
            "data_envio": registro.data_envio,
            "data_retorno": registro.data_retorno,
            "mensagem_erro": registro.mensagem_erro,
        }
        for registro in (
            session.query(EsocialDesligamento)
            .order_by(EsocialDesligamento.id)
            .all()
        )
    ]


col1, col2, col3 = st.columns(3)

col1.metric("Total de registros", total_registros)
col2.metric("Eventos com ID", total_com_id)
col3.metric("Eventos com XML", total_com_xml)


# ==========================================================
# PROCESSAMENTO DOS EVENTOS
# ==========================================================

st.divider()

st.subheader("⚙️ Processamento dos eventos S-2299")

st.write(
    """
    Esta etapa prepara os XMLs pendentes, realiza a assinatura digital,
    verifica a assinatura e valida os arquivos no esquema XSD do eSocial.
    XMLs já existentes não serão gerados novamente e XMLs já assinados
    não serão assinados novamente.
    """
)

if st.button(
    "🚀 Preparar, assinar e validar eventos",
    type="primary"
):

    try:

        with SessionLocal() as session:

            with st.spinner(
                "Processando eventos. Aguarde a conclusão..."
            ):

                resultado = processar_eventos(session)

        st.success("Processamento concluído!")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "XMLs preparados",
            resultado["preparados"]
        )

        col2.metric(
            "XMLs assinados",
            resultado["assinados"]
        )

        col3.metric(
            "XMLs validados",
            resultado["validos"]
        )

        if resultado["erros"]:

            st.warning(
                f'{len(resultado["erros"])} eventos apresentaram erros.'
            )

            df_erros = pd.DataFrame(resultado["erros"])

            st.dataframe(
                df_erros,
                use_container_width=True
            )

            csv_erros = df_erros.to_csv(
                index=False,
                sep=";"
            ).encode("utf-8-sig")

            st.download_button(
                label="📥 Baixar relatório de erros",
                data=csv_erros,
                file_name="erros_processamento_esocial.csv",
                mime="text/csv"
            )

        else:

            st.success(
                "Todos os eventos foram processados sem erros!"
            )

    except Exception as e:

        st.error(f"Erro no processamento: {e}")



# ==========================================================
# SELEÇÃO DOS EVENTOS PARA ENVIO
# ==========================================================

st.divider()

st.subheader("📦 Seleção dos eventos para envio")

st.write(
    "Selecione os eventos S-2299 que deseja incluir no próximo lote."
)

# Busca eventos pendentes que possuem ID e XML assinado
with SessionLocal() as session:

    registros_envio = (
        session.query(EsocialDesligamento)
        .filter(
            EsocialDesligamento.id_evento.is_not(None),
            EsocialDesligamento.xml.is_not(None),
            EsocialDesligamento.xml != "",
            EsocialDesligamento.status == "PENDENTE",
        )
        .order_by(EsocialDesligamento.id)
        .all()
    )

    dados_selecao = []

    for registro in registros_envio:

        try:
            raiz = etree.fromstring(
                registro.xml.encode("UTF-8")
            )

            assinaturas = raiz.xpath(
                ".//*[local-name()='Signature']"
            )

            # Só disponibiliza XML com uma assinatura
            if len(assinaturas) == 1:

                dados_selecao.append({
                    "Selecionar": False,
                    "ID": registro.id,
                    "Matrícula": registro.matricula,
                    "CPF": registro.cpf_trab,
                    "Data desligamento": registro.dt_deslig,
                    "Motivo": registro.mtv_deslig,
                    "Status": registro.status,
                    "ID evento": registro.id_evento,
                })

        except Exception:
            continue


df_selecao = pd.DataFrame(dados_selecao)

if not df_selecao.empty:

    st.info(
        f"{len(df_selecao)} eventos disponíveis para seleção."
    )

    # Opção para selecionar todos
    selecionar_todos = st.checkbox(
        "Selecionar todos os eventos",
        key="selecionar_todos_eventos"
    )

    # Prepara a tabela
    df_selecao["Selecionar"] = selecionar_todos

    # Tabela interativa
    df_editado = st.data_editor(
        df_selecao,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key=f"tabela_selecao_{selecionar_todos}",
        disabled=[
            "ID",
            "Matrícula",
            "CPF",
            "Data desligamento",
            "Motivo",
            "Status",
            "ID evento",
        ],
        column_config={
            "Selecionar": st.column_config.CheckboxColumn(
                "Selecionar",
                help="Marque os eventos que deseja enviar.",
                default=False,
            ),
            "ID": None,
        },
    )

    # Recupera somente os registros marcados
    df_marcados = df_editado[
        df_editado["Selecionar"] == True
    ]

    quantidade_selecionada = len(df_marcados)

    st.divider()

    col1, col2 = st.columns(2)

    col1.metric(
        "Eventos disponíveis",
        len(df_selecao)
    )

    col2.metric(
        "Eventos selecionados",
        quantidade_selecionada
    )

    # Confirma seleção
    if st.button(
        "📦 Confirmar seleção para envio",
        type="primary",
        disabled=quantidade_selecionada == 0,
    ):

        ids_selecionados = (
            df_marcados["ID"].astype(int).tolist()
        )

        st.session_state["eventos_selecionados"] = (
            ids_selecionados
        )

        st.success(
            f"{len(ids_selecionados)} eventos selecionados para montagem do lote."
        )

    # Exibe seleção já confirmada
    ids_confirmados = st.session_state.get(
        "eventos_selecionados",
        []
    )

    if ids_confirmados:

        st.success(
            f"{len(ids_confirmados)} eventos confirmados para envio."
        )

        if st.button("❌ Limpar seleção"):

            st.session_state["eventos_selecionados"] = []
            st.rerun()

else:

    st.warning(
        "Não existem eventos pendentes com XML assinado disponíveis para seleção."
    )





# ==========================================================
# EXPORTAÇÃO
# ==========================================================

st.divider()

st.subheader("📤 Exportação dos registros")

df_download = pd.DataFrame(dados)

'''st.dataframe(
    df_download,
    use_container_width=True
)'''

csv = df_download.to_csv(
    index=False,
    sep=";"
).encode("utf-8-sig")

st.download_button(
    label="⬇️ Baixar CSV dos desligamentos",
    data=csv,
    file_name="esocial_desligamento.csv",
    mime="text/csv"
)
