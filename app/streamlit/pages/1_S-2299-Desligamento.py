import streamlit as st
import pandas as pd
from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento
from app.etl.extract.desligamento import extract
from app.etl.load.desligamento import load
from app.etl.transform.desligamento import transformar_desligamento

st.set_page_config(
    page_title="eSocial",
    page_icon="📋",
    layout="wide"
)

st.title("📋 eSocial - S-2299-Desligamentos")

st.subheader("Carga de desligamentos")

if st.button(
    "🚀 Carregar desligamentos",
   ## type="primary",
    
):

    try:

        with st.spinner("Extraindo dados do banco source..."):

            df = extract()

               
        with st.spinner("Transformando desligamentos..."):

            with SessionLocal() as session:
                eventos = transformar_desligamento(session)
                qtd_eventos = session.query(EsocialDesligamento).count()
                st.info(
                    f'{qtd_eventos} Carregado prontos para envio'
                )

        

        st.success(
            "Carga concluída com sucesso!"
        )

    except Exception as e:

        st.error(
            f"Erro durante a carga: {e}"
        )
st.subheader("Exportação")

with SessionLocal() as session:

    registros = session.query(
        EsocialDesligamento
    ).all()

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
        for registro in registros
    ]

# Converte a lista para DataFrame
df_download = pd.DataFrame(dados)

# Converte o DataFrame para CSV
csv = df_download.to_csv(
    index=False,
    sep=";"
).encode("utf-8-sig")

# Mostra os dados na tela
st.dataframe(df_download,use_container_width=True)

# Botão para baixar CSV
st.download_button(
    label="⬇️ Baixar CSV",
    data=csv,
    file_name="esocial_desligamento.csv",
    mime="text/csv"
)