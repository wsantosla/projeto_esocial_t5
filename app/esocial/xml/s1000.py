from lxml import etree

from app.esocial.xml.id_evento import gerar_id_evento

NS = (
    "http://www.esocial.gov.br/schema/"
    "evt/evtInfoEmpregador/v_S_01_03_00"
)


def gerar_xml_s1000():

    id_evento = gerar_id_evento()

    root = etree.Element(
        f"{{{NS}}}eSocial",
        nsmap={None: NS}
    )

    evento = etree.SubElement(
        root,
        f"{{{NS}}}evtInfoEmpregador",
        Id=id_evento
    )

    ide_evento = etree.SubElement(
        evento,
        f"{{{NS}}}ideEvento"
    )

    etree.SubElement(
        ide_evento,
        f"{{{NS}}}tpAmb"
    ).text = "2"

    etree.SubElement(
        ide_evento,
        f"{{{NS}}}procEmi"
    ).text = "3"

    etree.SubElement(
        ide_evento,
        f"{{{NS}}}verProc"
    ).text = "1.0"

    ide_empregador = etree.SubElement(
        evento,
        f"{{{NS}}}ideEmpregador"
    )

    etree.SubElement(
        ide_empregador,
        f"{{{NS}}}tpInsc"
    ).text = "1"

    etree.SubElement(
        ide_empregador,
        f"{{{NS}}}nrInsc"
    ).text = "08806721"

    info_empregador = etree.SubElement(
        evento,
        f"{{{NS}}}infoEmpregador"
    )

    inclusao = etree.SubElement(
        info_empregador,
        f"{{{NS}}}inclusao"
    )

    ide_periodo = etree.SubElement(
        inclusao,
        f"{{{NS}}}idePeriodo"
    )

    etree.SubElement(
        ide_periodo,
        f"{{{NS}}}iniValid"
    ).text = "2021-07"

    info_cadastro = etree.SubElement(
        inclusao,
        f"{{{NS}}}infoCadastro"
    )

    campos = {
        "classTrib": "85",
        "indCoop": "0",
        "indConstr": "0",
        "indDesFolha": "0",
        "indOptRegEletron": "1",
        "cnpjEFR": "08778326000156",
    }

    for campo, valor in campos.items():
        etree.SubElement(
            info_cadastro,
            f"{{{NS}}}{campo}"
        ).text = valor

    return etree.tostring(
        root,
        encoding="unicode",
        pretty_print=True
    )
