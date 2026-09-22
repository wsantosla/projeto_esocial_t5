from lxml import etree
from app.config.esocial import SOAP_ACTION, SOAP_ENV,ESOCIAL_WS_NAMESPACE

def criar_envelope_soap(lote_xml):
    lote = etree.fromstring(lote_xml)
    envelope=etree.Element(
        f"{{{SOAP_ENV}}}Envelope",
        nsmap={
            "soap": SOAP_ENV
        }
    )

    etree.SubElement(
        envelope,
        f"{{{SOAP_ENV}}}Header"
    )

    body = etree.SubElement(
        envelope,
        f"{{{SOAP_ENV}}}Body"
    )

    enviar = etree.SubElement(
        body,
        f"{{{ESOCIAL_WS_NAMESPACE}}}EnviarLoteEventos"
    )

    lote_eventos = etree.SubElement(
        enviar,
        f"{{{ESOCIAL_WS_NAMESPACE}}}loteEventos"
    )

    lote_eventos.append(lote)

    return etree.tostring(
        envelope,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True
    )