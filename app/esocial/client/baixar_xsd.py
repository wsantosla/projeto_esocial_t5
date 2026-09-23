import requests

from app.config.esocial import URL_CONSULTA
from app.esocial.signature.certificado import carregar_certificado
from app.esocial.client.certificado_https import preparar_certificado_https


chave_privada, certificado, _ = carregar_certificado()

caminho_certificado, caminho_chave = preparar_certificado_https(
    chave_privada,
    certificado
)

url = URL_CONSULTA + "?xsd=xsd1"

print("Acessando:")
print(url)

resposta = requests.get(
    url,
    cert=(caminho_certificado, caminho_chave),
    timeout=60,
)

print("Status:", resposta.status_code)
print("Content-Type:", resposta.headers.get("Content-Type"))

print("\n========== RESPOSTA ==========\n")
print(resposta.text)