
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
            EsocialDesligamento.xml.is_not(None),
            EsocialDesligamento.xml != "",
            EsocialDesligamento.id_evento.is_not(None)
        )
        .order_by(EsocialDesligamento.id)
        .yield_per(100)
    )

    validos = 0
    erros = []

    for evento in eventos:

        try:

            xml_bytes = evento.xml.encode("UTF-8")

            validar_xml_desligamento(
                xml_bytes,
                schema
            )

            validos += 1

        except Exception as e:

            erros.append({
                "id": evento.id,
                "matricula": evento.matricula,
                "id_evento": evento.id_evento,
                "erro": str(e)
            })

    return validos, erros


if __name__ == "__main__":

    from app.database.local.connection import SessionLocal

    session = SessionLocal()

    try:

        validos, erros = validar_todos_eventos(session)

        print("\n===== RESULTADO DA VALIDAÇÃO XSD =====")

        print(f"XMLs válidos: {validos}")
        print(f"XMLs inválidos: {len(erros)}")

        if erros:

            print("\n===== ERROS ENCONTRADOS =====")

            for erro in erros[:20]:

                print(
                    f"ID: {erro['id']} | "
                    f"Matrícula: {erro['matricula']} | "
                    f"Erro: {erro['erro']}"
                )

    finally:
        session.close()