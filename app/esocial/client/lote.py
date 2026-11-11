
from lxml import etree

from app.config.esocial import (
    ESOCIAL_TP_INSC,
    ESOCIAL_NR_INSC,
    ESOCIAL_TRANSMISSOR_NR_INSC,
    ESOCIAL_TRANSMISSOR_TP_INSC,
)

NS_LOTE = (
    "http://www.esocial.gov.br/"
    "schema/lote/eventos/envio/v1_1_1"
)


def gerar_lote_eventos(xml, id_evento, grupo):

    if not xml:
        raise ValueError("Evento não possui XML.")

    if not id_evento:
        raise ValueError("Evento não possui ID.")

    if grupo not in ("1", "2", "3"):
        raise ValueError(f"Grupo inválido: {grupo}")

    xml_evento = etree.fromstring(
        xml.encode("UTF-8") if isinstance(xml, str) else xml
    )

    # Identifica o evento dentro do XML.
    elementos_evento = [
        elemento
        for elemento in xml_evento
        if etree.QName(elemento).localname.startswith("evt")
    ]

    if len(elementos_evento) != 1:
        raise ValueError("Não foi possível identificar o evento.")

    elemento_evento = elementos_evento[0]

    id_xml = elemento_evento.get("Id")

    if id_xml != id_evento:
        raise ValueError("ID informado diferente do ID do XML.")

    # Identificação do empregador.
    if ESOCIAL_TP_INSC == "1":
        nr_inscricao_empregador = ESOCIAL_NR_INSC[:8]
    else:
        nr_inscricao_empregador = ESOCIAL_NR_INSC

    eSocial = etree.Element(
        f"{{{NS_LOTE}}}eSocial",
        nsmap={None: NS_LOTE},
    )

    envio = etree.SubElement(
        eSocial,
        f"{{{NS_LOTE}}}envioLoteEventos",
        grupo=grupo,
    )

    ide_empregador = etree.SubElement(
        envio,
        f"{{{NS_LOTE}}}ideEmpregador",
    )

    etree.SubElement(
        ide_empregador,
        f"{{{NS_LOTE}}}tpInsc",
    ).text = ESOCIAL_TP_INSC

    etree.SubElement(
        ide_empregador,
        f"{{{NS_LOTE}}}nrInsc",
    ).text = nr_inscricao_empregador

    ide_transmissor = etree.SubElement(
        envio,
        f"{{{NS_LOTE}}}ideTransmissor",
    )

    etree.SubElement(
        ide_transmissor,
        f"{{{NS_LOTE}}}tpInsc",
    ).text = ESOCIAL_TRANSMISSOR_TP_INSC

    etree.SubElement(
        ide_transmissor,
        f"{{{NS_LOTE}}}nrInsc",
    ).text = ESOCIAL_TRANSMISSOR_NR_INSC

    eventos = etree.SubElement(
        envio,
        f"{{{NS_LOTE}}}eventos",
    )

    evento_lote = etree.SubElement(
        eventos,
        f"{{{NS_LOTE}}}evento",
        Id=id_evento,
    )

    evento_lote.append(xml_evento)

    return etree.tostring(
        eSocial,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True,
    )
