import requests

from datetime import datetime
from lxml import etree

from app.config.esocial import URL_ENVIO, SOAP_ACTION

from app.esocial.signature.certificado import carregar_certificado

from app.esocial.client.certificado_https import (
    preparar_certificado_https
)

from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento


NS_RETORNO = (
    "http://www.esocial.gov.br/schema/"
    "lote/eventos/envio/retornoEnvio/v1_1_0"
)


def extrair_dados_retorno(xml_resposta):

    root = etree.fromstring(xml_resposta)

    cd_resposta = root.findtext(
        ".//ret:cdResposta",
        namespaces={
            "ret": NS_RETORNO
        }
    )

    desc_resposta = root.findtext(
        ".//ret:descResposta",
        namespaces={
            "ret": NS_RETORNO
        }
    )

    protocolo = root.findtext(
        ".//ret:protocoloEnvio",
        namespaces={
            "ret": NS_RETORNO
        }
    )

    return (
        cd_resposta,
        desc_resposta,
        protocolo
    )


def salvar_retorno_envio(
    id_evento,
    protocolo,
    cd_resposta,
    desc_resposta
):

    with SessionLocal() as session:

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.id_evento == id_evento
            )
            .first()
        )

        if evento is None:
            raise ValueError(
                f"Evento não encontrado no banco: {id_evento}"
            )

        evento.data_envio = datetime.now()

        if cd_resposta == "201":

            evento.protocolo_envio = protocolo
            evento.status = "ENVIADO"
            evento.mensagem_erro = None

        else:

            evento.status = "ERRO_ENVIO"
            evento.mensagem_erro = (
                f"{cd_resposta} - {desc_resposta}"
            )

        session.commit()

        print("\n=======================================")
        print("RETORNO SALVO NO BANCO")
        print("=======================================")
        print(f"ID evento:       {id_evento}")
        print(f"Código resposta: {cd_resposta}")
        print(f"Descrição:       {desc_resposta}")
        print(f"Protocolo:       {protocolo}")
        print(f"Status:          {evento.status}")
        print("=======================================")


def enviar_soap(soap_xml, id_evento):

    print("Preparando certificado")

    chave_privada, certificado, _ = (
        carregar_certificado()
    )

    caminho_certificado, caminho_chave = (
        preparar_certificado_https(
            chave_privada,
            certificado
        )
    )

    print("Certificado preparado")

    print("Enviado para:")
    print(URL_ENVIO)

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f'"{SOAP_ACTION}"',
    }

    resposta = requests.post(
        URL_ENVIO,
        data=soap_xml,
        headers=headers,
        cert=(
            caminho_certificado,
            caminho_chave
        ),
        timeout=60,
    )

    print("\n=== RESPOSTA DO ESOCIAL ===")

    print(
        "Status HTTP:",
        resposta.status_code
    )

    print(
        "Content-Type:",
        resposta.headers.get("Content-Type")
    )

    print("\n--- Corpo da resposta ---\n")

    print(resposta.text)

    if resposta.status_code != 200:

        raise ValueError(
            f"Erro HTTP no envio: "
            f"{resposta.status_code}"
        )

    (
        cd_resposta,
        desc_resposta,
        protocolo
    ) = extrair_dados_retorno(
        resposta.content
    )

    print("\n=== DADOS EXTRAÍDOS ===")

    print(
        "Código:",
        cd_resposta
    )

    print(
        "Descrição:",
        desc_resposta
    )

    print(
        "Protocolo:",
        protocolo
    )

    print(
        "ID evento:",
        id_evento
    )

    if cd_resposta == "201":

        if not protocolo:
            raise ValueError(
                "eSocial retornou 201, "
                "mas o protocoloEnvio não foi encontrado."
            )

        salvar_retorno_envio(
            id_evento=id_evento,
            protocolo=protocolo,
            cd_resposta=cd_resposta,
            desc_resposta=desc_resposta
        )

        print(
            "\nEnvio concluído com sucesso."
        )

    else:

        print(
            "\nLote não aceito pelo eSocial."
        )

        salvar_retorno_envio(
            id_evento=id_evento,
            protocolo=protocolo,
            cd_resposta=cd_resposta,
            desc_resposta=desc_resposta
        )

    return resposta