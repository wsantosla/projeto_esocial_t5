from pathlib import Path
from cryptography.hazmat.primitives.serialization import pkcs12
from app.config.esocial import ESOCIAL_CERT_PASSWORD,ESOCIAL_CERT_PATH

def carregar_certificado():
    if not ESOCIAL_CERT_PATH:
        raise ValueError(
            "Esocial cer não configurado"
        )
    if not ESOCIAL_CERT_PASSWORD:
        raise ValueError(
            "Esocial cert password não encontrado:"
        )
    caminho = Path(ESOCIAL_CERT_PATH)
    if not caminho.exists():
        raise FileNotFoundError(
            f"Certificado não encontrado:{caminho}"
        )
    with open(caminho,"rb") as arquivo:
        dados_pfx = arquivo.read()

    senha = ESOCIAL_CERT_PASSWORD.encode("utf-8")

    chave_privada,certificado,certificados_adicionais=(
        pkcs12.load_key_and_certificates(dados_pfx,
                                         senha,
                                         )
    )

    if chave_privada is None:
        raise ValueError(
            "O certificado não possui chave privada"
        )
    if certificado is None:
        raise ValueError(
            "Certificado Digital não encontrado no arquivo."
        )
    return(chave_privada,
           certificado,
           certificados_adicionais)

if __name__ == "__main__":

    chave, certificado, adicionais = carregar_certificado()

    print("Certificado carregado com sucesso!")

    print(
        "Titular:",
        certificado.subject.rfc4514_string()
    )

    print(
        "Emissor:",
        certificado.issuer.rfc4514_string()
    )

    print(
        "Certificados adicionais:",
        len(adicionais or [])
    )