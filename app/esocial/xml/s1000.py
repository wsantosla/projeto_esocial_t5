
from lxml import etree

from app.esocial.xml.id_evento import gerar_id_evento

from app.config.esocial import (
    ESOCIAL_TP_AMB,
    ESOCIAL_PROC_EMI,
    ESOCIAL_VER_PROC,
    ESOCIAL_TP_INSC,
    ESOCIAL_NR_INSC,
)

NS = (
    "http://www.esocial.gov.br/schema/"
    "evt/evtInfoEmpregador/v_S_01_03_00"
)


def gerar_xml_s1000():

    id_evento = gerar_id_evento()

    # Validação das configurações obrigatórias
    configuracoes = {
        "ESOCIAL_TP_AMB": ESOCIAL_TP_AMB,
        "ESOCIAL_PROC_EMI": ESOCIAL_PROC_EMI,
        "ESOCIAL_VER_PROC": ESOCIAL_VER_PROC,
        "ESOCIAL_TP_INSC": ESOCIAL_TP_INSC,
        "ESOCIAL_NR_INSC": ESOCIAL_NR_INSC,
    }

    for nome, valor in configuracoes.items():
        if not valor:
            raise ValueError(
                f"A configuração {nome} não foi definida no .env."
            )

    # Para CNPJ, o S-1000 utiliza os 8 primeiros dígitos.
    if ESOCIAL_TP_INSC == "1":
        nr_inscricao = ESOCIAL_NR_INSC[:8]
    else:
        nr_inscricao = ESOCIAL_NR_INSC

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
    ).text = ESOCIAL_TP_AMB

    etree.SubElement(
        ide_evento,
        f"{{{NS}}}procEmi"
    ).text = ESOCIAL_PROC_EMI

    etree.SubElement(
        ide_evento,
        f"{{{NS}}}verProc"
    ).text = ESOCIAL_VER_PROC

    ide_empregador = etree.SubElement(
        evento,
        f"{{{NS}}}ideEmpregador"
    )

    etree.SubElement(
        ide_empregador,
        f"{{{NS}}}tpInsc"
    ).text = ESOCIAL_TP_INSC

    etree.SubElement(
        ide_empregador,
        f"{{{NS}}}nrInsc"
    ).text = nr_inscricao

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
