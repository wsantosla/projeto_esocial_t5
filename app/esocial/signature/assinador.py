
from lxml import etree
from signxml import XMLSigner, XMLVerifier, methods
from cryptography.hazmat.primitives.serialization import Encoding
from app.esocial.signature.certificado import carregar_certificado
from app.database.local.models import EsocialDesligamento




def assinar_xml(xml, chave_privada, certificado):

    raiz = etree.fromstring(xml)

    # Remove qualquer assinatura existente
    # antes de gerar uma nova.
    assinaturas = raiz.xpath(
        ".//*[local-name()='Signature']"
    )

    for assinatura in assinaturas:
        pai = assinatura.getparent()
        if pai is not None:
            pai.remove(assinatura)

    certificado_pem = certificado.public_bytes(
        Encoding.PEM
    )

    C14N_ESOCIAL = (
        "http://www.w3.org/TR/2001/"
        "REC-xml-c14n-20010315"
    )

    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm=C14N_ESOCIAL,
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



def assinar_e_salvar_xml(evento, session, chave_privada, certificado):

    if not evento.xml:
        raise ValueError("Evento não possui XML para assinatura.")

    xml_assinado = assinar_xml(
        evento.xml.encode("UTF-8"),
        chave_privada,
        certificado,
    )

    # Confirma a assinatura antes de salvar
    verificar_assinatura(
        xml_assinado,
        certificado
    )

    evento.xml = xml_assinado.decode("UTF-8")

    return xml_assinado



def verificar_assinatura(xml, certificado):

    raiz = etree.fromstring(xml)

    assinaturas = raiz.xpath(
        ".//*[local-name()='Signature']"
    )

    print(
        f"\nQuantidade de assinaturas encontradas: "
        f"{len(assinaturas)}"
    )

    if len(assinaturas) != 1:
        raise ValueError(
            f"O XML deve possuir exatamente 1 assinatura. "
            f"Foram encontradas {len(assinaturas)}."
        )

    XMLVerifier().verify(
        raiz,
        x509_cert=certificado
    )

    return True
def assinar_todos_eventos(session):

    # Carrega o certificado apenas uma vez
    chave_privada, certificado, _ = carregar_certificado()

    eventos = (
        session.query(EsocialDesligamento)
        .filter(
            EsocialDesligamento.xml.is_not(None),
            EsocialDesligamento.id_evento.is_not(None),
        )
        .all()
    )

    assinados = 0
    ignorados = 0
    erros = []

    for evento in eventos:

        try:

            raiz = etree.fromstring(
                evento.xml.encode("UTF-8")
            )

            # Não assina novamente um XML já assinado
            assinatura_existente = raiz.xpath(
                ".//*[local-name()='Signature']"
            )

            if assinatura_existente:
                ignorados += 1
                continue

            assinar_e_salvar_xml(
                evento,
                session,
                chave_privada,
                certificado
            )

            assinados += 1

            # Salva em blocos de 100 eventos
            if assinados % 100 == 0:
                session.commit()

        except Exception as e:

            session.rollback()

            erros.append({
                "matricula": evento.matricula,
                "id_evento": evento.id_evento,
                "erro": str(e)
            })

    session.commit()

    return assinados, ignorados, erros

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

            print("\n=== GERANDO NOVA ASSINATURA ===")

            # IMPORTANTE:
            # gera novamente a assinatura usando a função atualizada
            xml_assinado = assinar_e_salvar_xml(
                evento,
                session
            )

            print("\n=== ASSINATURA GERADA ===\n")

            print(xml_assinado.decode("UTF-8"))

            # verifica a nova assinatura
            _, certificado, _ = carregar_certificado()

            print("\n=== VERIFICANDO ASSINATURA ===")

            verificar_assinatura(
                xml_assinado,
                certificado
            )

            print("\nAssinatura digital válida!")

    finally:
        session.close()