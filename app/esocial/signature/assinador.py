from lxml import etree

from signxml import XMLSigner, methods,XMLVerifier

from cryptography.hazmat.primitives.serialization import Encoding


def assinar_xml(xml, chave_privada, certificado):

    raiz = etree.fromstring(xml)

    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
    )

    certificado_pem = certificado.public_bytes(
        Encoding.PEM
    )

    xml_assinado = signer.sign(
        raiz,
        key=chave_privada,
        cert=certificado_pem,
    )

    return etree.tostring(
        xml_assinado,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True,
    )

def assinar_e_salvar_xml(evento,session):
    chave_privada, certificado,_ = carregar_certificado()

    xml_assinado = assinar_xml(
        evento.xml.encode("UTF-8"),
        chave_privada,
        certificado,
        
    )
    evento.xml = xml_assinado.decode("UTF-8")

    session.commit()

    return xml_assinado

def verificar_assinatura(xml,certificado):
    raiz = etree.fromstring(xml)
    XMLVerifier().verify(
        raiz,
        x509_cert=certificado,
    )

    return True


if __name__ == "__main__":

    from app.database.local.connection import SessionLocal
    from app.database.local.models import EsocialDesligamento
    from app.esocial.signature.certificado import carregar_certificado

    session = SessionLocal()

    try:

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.is_not(None),
                EsocialDesligamento.id_evento.is_not(None),
            )
            .first()
        )

        if not evento:

            print("Nenhum evento encontrado.")

        else:

            print("Matrícula:", evento.matricula)
            print("Id:", evento.id_evento)

            _, certificado, _ = carregar_certificado()

            print("\nVerificando assinatura...")

            verificar_assinatura(
                evento.xml.encode("UTF-8"),
                certificado,
            )

            print("\nAssinatura digital válida!")

    finally:

        session.close()