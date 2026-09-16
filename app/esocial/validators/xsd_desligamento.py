from pathlib import Path
from lxml import etree

def validar_xml_desligamento(xml):

    RAIZ_PROJETO = Path(__file__).resolve().parents[2]

    caminho_xsd = (
    RAIZ_PROJETO
    / "esquemas_xsd"
    / "v_S_01_03_00"
    / "evtDeslig.xsd"
    )
    if not caminho_xsd.exists():
        raise FileNotFoundError(
            f"XSD não encontrado:{caminho_xsd}"
        )
    schema_doc = etree.parse(caminho_xsd)
    schema = etree.XMLSchema(schema_doc)
    xml_doc = etree.fromstring(xml)
    schema.assertValid(xml_doc)

    return True

if __name__ == "__main__":

    from app.database.local.connection import SessionLocal
    from app.database.local.models import EsocialDesligamento

    session = SessionLocal()

    try:

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.is_not(None)
            )
            .first()
        )

        if not evento:

            print("Nenhum XML encontrado no banco.")

        else:

            print("Matrícula:", evento.matricula)
            print("Id:", evento.id_evento)
            print("\nValidando XML...\n")

            try:

                validar_xml_desligamento(
                    evento.xml.encode("UTF-8")
                )

                print("XML válido segundo o XSD!")

            except etree.DocumentInvalid as erro:

                print("XML inválido!")
                print("\nErros encontrados:")

                for erro_xsd in erro.error_log:
                    print(
                        f"Linha {erro_xsd.line}: "
                        f"{erro_xsd.message}"
                    )

    finally:

        session.close()