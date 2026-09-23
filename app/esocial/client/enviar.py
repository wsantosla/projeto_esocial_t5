import requests

from app.config.esocial import URL_ENVIO,SOAP_ACTION

from app.esocial.signature.certificado import carregar_certificado

from app.esocial.client.certificado_https import preparar_certificado_https

def enviar_soap(soap_xml):
    print("Preaparando certificado")
    chave_privada,certificado,_= carregar_certificado()
    caminho_certificado,caminho_chave=(
        preparar_certificado_https(chave_privada,certificado)
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
        cert=(caminho_certificado,caminho_chave),
        timeout=60,
    )

    print("\n===RESPOSTA DO ESOCIAL====")
    print("Status HTTP:",resposta.status_code)
    print("Content-Type:",resposta.headers.get("Content-Type"))

    print("\n---Corpo da resposta--\n")

    print(resposta.text)

    return resposta