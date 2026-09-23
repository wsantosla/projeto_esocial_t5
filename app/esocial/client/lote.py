from lxml import etree
from app.config.esocial import ESOCIAL_TP_INSC,ESOCIAL_NR_INSC,ESOCIAL_TRANSMISSOR_NR_INSC,ESOCIAL_TRANSMISSOR_TP_INSC

NS_LOTE=(
    "http://www.esocial.gov.br/"
    "schema/lote/eventos/envio/v1_1_1"
    )

def gerar_lote_eventos(evento):

    if not evento.xml:
        raise ValueError(
            "Evento não possui XML"
         )
    if not evento.id_evento:
        raise ValueError(
            "Evento não possui id"
        )
    xml_evento =etree.fromstring(
        evento.xml.encode("UTF-8")
    )

    eSocial = etree.Element(
        f"{{{NS_LOTE}}}eSocial",
        nsmap={None:NS_LOTE},
    )

    envioLoteEventos=etree.SubElement(
        eSocial,
        f"{{{NS_LOTE}}}envioLoteEventos"
    )

    envioLoteEventos.set(
        "grupo",
        "2"
    )

    #Empregador
    idEmpregador = etree.SubElement(
        envioLoteEventos,
        f"{{{NS_LOTE}}}ideEmpregador"
    )
    etree.SubElement(
            idEmpregador,
            f"{{{NS_LOTE}}}tpInsc",
        ).text = ESOCIAL_TP_INSC

    
    etree.SubElement(
        idEmpregador,
        f"{{{NS_LOTE}}}nrInsc",
    ).text = ESOCIAL_NR_INSC

    #tranmissor

    ideTransmissor = etree.SubElement(
        envioLoteEventos,
        f"{{{NS_LOTE}}}ideTransmissor",
    )

    etree.SubElement(
        ideTransmissor,
        f"{{{NS_LOTE}}}tpInsc",
    ).text=ESOCIAL_TRANSMISSOR_TP_INSC


    etree.SubElement(
        ideTransmissor,
        f"{{{NS_LOTE}}}nrInsc",
    ).text =ESOCIAL_TRANSMISSOR_NR_INSC

    #Eventos

    eventos = etree.SubElement(
        envioLoteEventos,
        f"{{{NS_LOTE}}}eventos",
    )
    evento_lote = etree.SubElement(
        eventos,
        f"{{{NS_LOTE}}}evento",
    )

    evento_lote.set(
        "Id",
        evento.id_evento,
    )
     # Coloca o XML S-2299 assinado dentro do lote
    evento_lote.append(
        xml_evento
    )

    return etree.tostring(
        eSocial,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True,
    )