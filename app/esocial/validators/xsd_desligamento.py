
from pathlib import Path
from lxml import etree


def carregar_schema_desligamento():

    RAIZ_PROJETO = Path(__file__).resolve().parents[2]

    caminho_xsd = (
        RAIZ_PROJETO
        / "esquemas_xsd"
        / "v_S_01_03_00"
        / "evtDeslig.xsd"
    )

    if not caminho_xsd.exists():
        raise FileNotFoundError(
            f"XSD não encontrado: {caminho_xsd}"
        )

    schema_doc = etree.parse(str(caminho_xsd))

    return etree.XMLSchema(schema_doc)


def validar_xml_desligamento(xml, schema=None):

    if schema is None:
        schema = carregar_schema_desligamento()

    xml_doc = etree.fromstring(xml)

    schema.assertValid(xml_doc)

    return True


from app.database.local.models import EsocialDesligamento


def validar_todos_eventos(session):

    schema = carregar_schema_desligamento()

    eventos = (
        session.query(EsocialDesligamento)
        .filter(
            EsocialDesligamento.xml.is_not(None)
        )
        .all()
    )

    validos = 0
    erros = []

    for evento in eventos:

        try:

            # Só aceita XML que tenha assinatura
            raiz = etree.fromstring(
                evento.xml.encode("UTF-8")
            )

            assinaturas = raiz.xpath(
                ".//*[local-name()='Signature']"
            )

            if len(assinaturas) != 1:
                raise ValueError(
                    "XML não possui exatamente uma assinatura."
                )

            validar_xml_desligamento(
                evento.xml.encode("UTF-8"),
                schema
            )

            validos += 1

        except Exception as e:

            erros.append({
                "matricula": evento.matricula,
                "id_evento": evento.id_evento,
                "erro": str(e)
            })

    return validos, erros
