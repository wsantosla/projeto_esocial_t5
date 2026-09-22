import requests

from app.config.esocial import URL_ENVIO
from app.esocial.signature.certificado import carregar_certificado
from app.esocial.client.certificado_https import preparar_certificado_https



def baixar_wsdl():

        chave_privada,certificado,_ = carregar_certificado()
        caminho_certificado,caminho_chave = (
            preparar_certificado_https(
                chave_privada,certificado,
            )
        )
        url_wsdl = URL_ENVIO + "?singleWsdl"
        print("Baixando Wsdl:")
        print(url_wsdl)

        resposta = requests.get(
            url_wsdl,
            cert=(caminho_certificado,caminho_chave,),timeout=30,
        )
        print("status:",resposta.status_code)

        resposta.raise_for_status()

        with open(
                "WsEnviarLoteEventos.wsdl",
                "wb",
            ) as arquivo:
                arquivo.write(resposta.content)
        print("WSDL salvo com sucesso;")

if __name__ == "__main__":
        baixar_wsdl()