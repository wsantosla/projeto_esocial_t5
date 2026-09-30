import requests
from app.database.local.models import EsocialDesligamento
from app.database.local.connection import SessionLocal

from app.config.esocial import (
    URL_CONSULTA,
    SOAP_ACTION_CONSULTA,
)
from app.esocial.client.processar_retorno import(processar_retorno_consulta)

from app.esocial.signature.certificado import carregar_certificado

from app.esocial.client.certificado_https import (
    preparar_certificado_https,
)


NS_CONSULTA = (
    "http://www.esocial.gov.br/schema/"
    "lote/eventos/envio/consulta/"
    "retornoProcessamento/v1_0_0"
)


def consultar_lote(protocolo):

    print("Preparando certificado...")

    chave_privada, certificado, _ = carregar_certificado()

    caminho_certificado, caminho_chave = (
        preparar_certificado_https(
            chave_privada,
            certificado
        )
    )

    print("Certificado preparado.")

    soap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>

<s:Envelope
    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

    <s:Body>

        <ConsultarLoteEventos
            xmlns="{NS_CONSULTA}">

            <consulta>

                <eSocial xmlns="{NS_CONSULTA}">

                    <consultaLoteEventos>

                        <protocoloEnvio>{protocolo}</protocoloEnvio>

                    </consultaLoteEventos>

                </eSocial>

            </consulta>

        </ConsultarLoteEventos>

    </s:Body>

</s:Envelope>
"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f'"{SOAP_ACTION_CONSULTA}"',
    }

    print("\n========== XML CONSULTA ==========\n")
    print(soap_xml)

    resposta = requests.post(
        URL_CONSULTA,
        data=soap_xml.encode("utf-8"),
        headers=headers,
        cert=(
            caminho_certificado,
            caminho_chave
        ),
        timeout=60,
    )

    print("\n========== RESPOSTA ==========\n")

    print(
        "Status HTTP:",
        resposta.status_code
    )

    print(
        "Content-Type:",
        resposta.headers.get("Content-Type")
    )

    print(resposta.text)

    resultado = processar_retorno_consulta(resposta.text)

    return resultado

if __name__ == "__main__":
    session=SessionLocal()
    registro = session.query(EsocialDesligamento).filter(
        EsocialDesligamento.protocolo_envio.is_not (None)
    ).first()

    protocolo= registro.protocolo_envio

    consultar_lote(protocolo)