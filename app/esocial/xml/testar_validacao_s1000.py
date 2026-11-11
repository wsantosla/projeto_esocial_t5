
from pathlib import Path
from app.esocial.xml.s1000 import gerar_xml_s1000
from app.esocial.signature.assinador import assinar_xml,verificar_assinatura
from app.esocial.signature.certificado import carregar_certificado
from app.esocial.validators.xsd_s1000 import validar_xml_s1000



BASE_DIR = Path(__file__).resolve().parents[2]

CAMINHO_XSD = (
    BASE_DIR
    / "esquemas_xsd"
    / "v_S_01_03_00"
    / "evtInfoEmpregador.xsd"
)


print("\n=== GERANDO XML S-1000 ===")

xml = gerar_xml_s1000()

print("\n=== ASSINANDO XML S-1000 ===")

chave_privada, certificado, _ = carregar_certificado()

xml_assinado = assinar_xml(
    xml.encode("UTF-8"),
    chave_privada,
    certificado,
)

xml_assinado_texto = xml_assinado.decode("UTF-8")

print("\n=== VALIDANDO XML ASSINADO NO XSD ===")

valido = validar_xml_s1000(
    xml=xml_assinado_texto,
    caminho_xsd=CAMINHO_XSD,
)

if valido:
    print("\nTeste concluído: XML assinado e aprovado pelo XSD.")
else:
    print("\nTeste concluído: corrija os erros apresentados.")

print("\n=== VERIFICANDO ASSINATURA DIGITAL ===")

verificar_assinatura(
    xml_assinado,
    certificado,
)

print("Assinatura digital válida!")


CAMINHO_XML = (
    Path(__file__).resolve().parents[2]
    / "xml_gerados"
    / "s1000_assinado.xml"
)

CAMINHO_XML.parent.mkdir(
    parents=True,
    exist_ok=True
)

CAMINHO_XML.write_bytes(xml_assinado)

print(f"XML assinado salvo em: {CAMINHO_XML}")