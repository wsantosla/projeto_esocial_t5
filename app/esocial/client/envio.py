import requests
from app.config.esocial import URL_ENVIO

def testar_conexao():
    print("URL:", repr(URL_ENVIO))

    resposta = requests.get(
        URL_ENVIO,
        timeout=30,
    )

    print("Status:",resposta.status_code)
    print("Url:",resposta.url)
    print("Resposta")
    print(resposta.text)

   
if __name__ == "__main__":
    testar_conexao()