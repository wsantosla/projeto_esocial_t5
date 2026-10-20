from lxml import etree

from app.esocial.xml.s1000 import gerar_xml_s1000

xml = gerar_xml_s1000()

documento = etree.fromstring(xml.encode("utf-8"))

id_evento = documento.find(
    ".//{*}evtInfoEmpregador"
).get("Id")

print(xml)
print("\nID gerado:", id_evento)
print("Tamanho do ID:", len(id_evento))

assert len(id_evento) == 36