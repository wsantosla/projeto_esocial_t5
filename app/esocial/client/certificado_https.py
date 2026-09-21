from pathlib import Path

from cryptography.hazmat.primitives import serialization

def preparar_certificado_https(
        chave_privada,
        certificado,
        caminho_certificado="certificado_esocial.pem",
        caminho_chave="chave_esocial.pem",

):
        caminho_certificado = Path(caminho_certificado)
        caminho_chave = Path(caminho_chave)

        caminho_certificado.write_bytes(
            certificado.public_bytes(
                serialization.Encoding.PEM
        )
    )
#chave privada
        caminho_chave.write_bytes(
                chave_privada.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                    
                )
        )
        return(
                str(caminho_certificado),
                str(caminho_chave),
        )