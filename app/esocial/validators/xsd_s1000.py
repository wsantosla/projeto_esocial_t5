
from pathlib import Path
from lxml import etree


def validar_xml_s1000(xml: str, caminho_xsd: str | Path) -> bool:
    caminho_xsd = Path(caminho_xsd)

    if not caminho_xsd.exists():
        raise FileNotFoundError(
            f"XSD do S-1000 não encontrado: {caminho_xsd}"
        )

    schema_doc = etree.parse(str(caminho_xsd))
    schema = etree.XMLSchema(schema_doc)

    documento = etree.fromstring(xml.encode("utf-8"))

    if schema.validate(documento):
        print("XML S-1000 válido conforme o XSD.")
        return True

    print("XML S-1000 inválido:")
    for erro in schema.error_log:
        print(f"Linha {erro.line}, coluna {erro.column}: {erro.message}")

    return False
