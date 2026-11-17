
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

def assinar_todos_eventos(session, tamanho_lote=100):

    # Carrega o certificado apenas uma vez
    chave_privada, certificado, _ = carregar_certificado()

    ultimo_id = 0

    assinados = 0
    ignorados = 0
    erros = []

    while True:

        eventos = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.id > ultimo_id,
                EsocialDesligamento.xml.is_not(None),
                EsocialDesligamento.xml != "",
                EsocialDesligamento.id_evento.is_not(None)
            )
            .order_by(EsocialDesligamento.id)
            .limit(tamanho_lote)
            .all()
        )

        if not eventos:
            break

        for evento in eventos:

            ultimo_id = evento.id

            try:

                raiz = etree.fromstring(
                    evento.xml.encode("UTF-8")
                )

                # Verifica se já existe assinatura
                assinatura_existente = raiz.xpath(
                    ".//*[local-name()='Signature']"
                )

                if assinatura_existente:
                    ignorados += 1
                    continue

                # Assina e verifica antes de salvar
                assinar_e_salvar_xml(
                    evento,
                    session,
                    chave_privada,
                    certificado
                )

                assinados += 1

            except Exception as e:

                erros.append({
                    "id": evento.id,
                    "matricula": evento.matricula,
                    "id_evento": evento.id_evento,
                    "erro": str(e)
                })

                print(
                    f"Erro ao assinar evento {evento.id}: {e}"
                )

        # Confirma cada lote de registros
        try:

            session.commit()

        except Exception:

            session.rollback()
            raise

        print(
            f"Processamento até o ID {ultimo_id} | "
            f"Assinados: {assinados} | "
            f"Ignorados: {ignorados} | "
            f"Erros: {len(erros)}"
        )

    return assinados, ignorados, erros



if __name__ == "__main__":

    from app.database.local.connection import SessionLocal

    session = SessionLocal()

    try:

        # Carrega o certificado
        chave_privada, certificado, _ = carregar_certificado()

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.is_not(None),
                EsocialDesligamento.id_evento.is_not(None)
            )
            .order_by(EsocialDesligamento.id)
            .first()
        )

        if not evento:

            print("Nenhum evento encontrado.")

        else:

            print("Matrícula:", evento.matricula)
            print("ID:", evento.id_evento)

            xml_assinado = assinar_e_salvar_xml(
                evento,
                session,
                chave_privada,
                certificado
            )

            session.commit()

            print("\nAssinatura gerada e salva!")

            verificar_assinatura(
                xml_assinado,
                certificado
            )

            print("\nAssinatura digital válida!")

    except Exception:

        session.rollback()
        raise

    finally:

        session.close()

if __name__ == "__main__":

    from app.database.local.connection import SessionLocal
    from app.esocial.validators.xsd_desligamento import (
        carregar_schema_desligamento,
        validar_xml_desligamento
    )

    session = SessionLocal()

    try:
        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.like("%<ds:Signature%")
            )
            .order_by(EsocialDesligamento.id)
            .first()
        )

        if not evento:
            print("Nenhum XML assinado encontrado.")
        else:
            _, certificado, _ = carregar_certificado()

            xml_bytes = evento.xml.encode("UTF-8")

            # Verificação criptográfica
            verificar_assinatura(xml_bytes, certificado)
            print("Assinatura digital válida!")

            # Validação do XSD
            schema = carregar_schema_desligamento()

            validar_xml_desligamento(xml_bytes, schema)
            print("XML válido no esquema XSD!")

    finally:
        session.close()