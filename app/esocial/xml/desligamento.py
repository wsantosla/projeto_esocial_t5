from lxml import etree

from app.config.esocial import (
    ESOCIAL_TP_AMB,
    ESOCIAL_PROC_EMI,
    ESOCIAL_VER_PROC,
    ESOCIAL_TP_INSC,
    ESOCIAL_NR_INSC,
)


NS = "http://www.esocial.gov.br/schema/evt/evtDeslig/v_S_01_03_00"

NSMAP = {
    None: NS
}


def gerar_xml_desligamento(evento):

    if not evento.id_evento:
        raise ValueError(
            "Evento ainda não possui id no eSocial"
        )

    eSocial = etree.Element(
        f"{{{NS}}}eSocial",
        nsmap=NSMAP
    )

    evtDeslig = etree.SubElement(
        eSocial,
        f"{{{NS}}}evtDeslig"
    )

    evtDeslig.set("Id", evento.id_evento)

    # ==========================
    # ideEvento
    # ==========================

    ideEvento = etree.SubElement(
        evtDeslig,
        f"{{{NS}}}ideEvento"
    )

    etree.SubElement(
        ideEvento,
        f"{{{NS}}}indRetif"
    ).text = "1"

    etree.SubElement(
        ideEvento,
        f"{{{NS}}}tpAmb"
    ).text = ESOCIAL_TP_AMB

    etree.SubElement(
        ideEvento,
        f"{{{NS}}}procEmi"
    ).text = ESOCIAL_PROC_EMI

    etree.SubElement(
        ideEvento,
        f"{{{NS}}}verProc"
    ).text = ESOCIAL_VER_PROC

    # ==========================
    # ideEmpregador
    # ==========================

    ideEmpregador = etree.SubElement(
        evtDeslig,
        f"{{{NS}}}ideEmpregador"
    )

    etree.SubElement(
        ideEmpregador,
        f"{{{NS}}}tpInsc"
    ).text = ESOCIAL_TP_INSC

    etree.SubElement(
        ideEmpregador,
        f"{{{NS}}}nrInsc"
    ).text = ESOCIAL_NR_INSC

    # ==========================
    # ideVinculo
    # ==========================

    ideVinculo = etree.SubElement(
        evtDeslig,
        f"{{{NS}}}ideVinculo"
    )

    etree.SubElement(
        ideVinculo,
        f"{{{NS}}}cpfTrab"
    ).text = evento.cpf_trab

    etree.SubElement(
        ideVinculo,
        f"{{{NS}}}matricula"
    ).text = evento.matricula

    # ==========================
    # infoDeslig
    # ==========================

    infoDeslig = etree.SubElement(
        evtDeslig,
        f"{{{NS}}}infoDeslig"
    )

    etree.SubElement(
        infoDeslig,
        f"{{{NS}}}mtvDeslig"
    ).text = evento.mtv_deslig

    etree.SubElement(
        infoDeslig,
        f"{{{NS}}}dtDeslig"
    ).text = evento.dt_deslig.isoformat()

    etree.SubElement(
        infoDeslig,
        f"{{{NS}}}indPagtoAPI"
    ).text = evento.ind_pagto_api

    return etree.tostring(
        eSocial,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True
    )

def gerar_e_salvar_xml(evento,session):

    xml = gerar_xml_desligamento(evento)
    evento.xml = xml.decode("UTF-8")

    session.commit()
    return xml
                       


if __name__ == "__main__":

    from app.database.local.connection import SessionLocal
    from app.database.local.models import EsocialDesligamento

    session = SessionLocal()

    try:

        evento = (
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.status == "PENDENTE",
                EsocialDesligamento.id_evento.is_not(None),
                EsocialDesligamento.xml.is_(None)
            )
            .first()
        )

        if not evento:
            print("Nenhum evento pendente encontrado.")
        else:

            
            xml = gerar_e_salvar_xml(evento,session)

            print("Xml salvo com sucesso")
            print(xml.decode("UTF-8"))

    finally:
        session.close()