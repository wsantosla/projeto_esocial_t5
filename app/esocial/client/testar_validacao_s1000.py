
from pathlib import Path
from lxml import etree

from app.esocial.xml.s1000 import gerar_xml_s1000

from app.esocial.signature.assinador import (
    assinar_xml,
    verificar_assinatura,
)

from app.esocial.signature.certificado import carregar_certificado

from app.esocial.validators.xsd_s1000 import validar_xml_s1000

from app.esocial.client.lote import gerar_lote_eventos

from app.esocial.client.validar_lote import validar_lote


# Caminhos
BASE_DIR = Path(__file__).resolve().parents[2]

CAMINHO_XSD = (
    BASE_DIR
    / "esquemas_xsd"
    / "v_S_01_03_00"
    / "evtInfoEmpregador.xsd"
)

CAMINHO_XML = (
    BASE_DIR
    / "xml_gerados"
    / "s1000_assinado.xml"
)

CAMINHO_LOTE = (
    BASE_DIR
    / "xml_gerados"
    / "lote_s1000.xml"
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

if not valido:
    raise ValueError("XML S-1000 não passou na validação XSD.")

print("XML S-1000 aprovado pelo XSD.")


print("\n=== VERIFICANDO ASSINATURA DIGITAL ===")

verificar_assinatura(
    xml_assinado,
    certificado,
)

print("Assinatura digital válida!")


print("\n=== GERANDO LOTE S-1000 ===")

raiz_evento = etree.fromstring(xml_assinado)

elementos_evento = [
    elemento
    for elemento in raiz_evento
    if etree.QName(elemento).localname == "evtInfoEmpregador"
]

if len(elementos_evento) != 1:
    raise ValueError("Não foi possível identificar o evento S-1000.")

id_evento = elementos_evento[0].get("Id")

if not id_evento:
    raise ValueError("ID do S-1000 não encontrado.")

lote = gerar_lote_eventos(
    xml=xml_assinado,
    id_evento=id_evento,
    grupo="1",
)


print("\n=== VALIDANDO ESTRUTURA DO LOTE ===")

validar_lote(
    lote,
    grupo_esperado="1",
)


print("\n=== SALVANDO ARQUIVOS ===")

CAMINHO_XML.parent.mkdir(
    parents=True,
    exist_ok=True,
)

CAMINHO_XML.write_bytes(xml_assinado)
CAMINHO_LOTE.write_bytes(lote)

print(f"XML assinado salvo em: {CAMINHO_XML}")
print(f"Lote S-1000 salvo em: {CAMINHO_LOTE}")

print("\n=== TESTE CONCLUÍDO ===")
