import requests
from app.config.esocial import URL_ENVIO
from app.esocial.signature.certificado import carregar_certificado
from app.esocial.client.certificado_https import preparar_certificado_https

def testar_conexao():
    print("URL:", repr(URL_ENVIO))

    chave_privada,certificado,_ = carregar_certificado()
    print("certificado_carregado")

    # prepara certificado e chave para https
    caminho_certificado,caminho_chave = (preparar_certificado_https(chave_privada,certificado))

    print("Certificado HTTPS preparado")

    resposta = requests.get(
        URL_ENVIO,cert=(caminho_certificado,caminho_chave),timeout=30,
    )


    print("Staturs:", resposta.status_code)
    print("URL:", resposta.url)
    print(resposta.text)
if __name__ == "__main__":
    testar_conexao()