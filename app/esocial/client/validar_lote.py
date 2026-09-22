from lxml import etree


def validar_lote(xml_lote):

    raiz = etree.fromstring(xml_lote)

    # 1. Verifica raiz
    if etree.QName(raiz).localname != "eSocial":
        raise ValueError(
            "Raiz do lote não é eSocial."
        )

    # 2. Procura envioLoteEventos
    envio = raiz.find(
        ".//{*}envioLoteEventos"
    )

    if envio is None:
        raise ValueError(
            "envioLoteEventos não encontrado."
        )

    # 3. Verifica grupo
    grupo = envio.get("grupo")

    if grupo != "2":
        raise ValueError(
            f"Grupo inválido: {grupo}"
        )

    # 4. Procura eventos
    eventos = envio.find(
        "{*}eventos"
    )

    if eventos is None:
        raise ValueError(
            "Grupo eventos não encontrado."
        )

    lista_eventos = eventos.findall(
        "{*}evento"
    )

    if not lista_eventos:
        raise ValueError(
            "Nenhum evento encontrado no lote."
        )

    print(
        f"Eventos encontrados: {len(lista_eventos)}"
    )

    # 5. Verifica cada evento
    for evento in lista_eventos:

        id_lote = evento.get("Id")

        print(
            "Id do evento no lote:",
            id_lote
        )

        xml_evento = evento.find(
            "{*}eSocial"
        )

        if xml_evento is None:
            raise ValueError(
                "XML do evento não encontrado."
            )

        evt_deslig = xml_evento.find(
            "{*}evtDeslig"
        )

        if evt_deslig is None:
            raise ValueError(
                "evtDeslig não encontrado."
            )

        id_evt = evt_deslig.get("Id")

        print(
            "Id do evtDeslig:",
            id_evt
        )

        if id_lote != id_evt:
            raise ValueError(
                "Os Ids do lote e do evento são diferentes."
            )

        # Verifica assinatura
       # Verifica assinatura
      # Verifica assinatura
        assinatura = xml_evento.find(
            "{http://www.w3.org/2000/09/xmldsig#}Signature"
        )

        if assinatura is None:
            raise ValueError(
                "Assinatura digital não encontrada."
            )

        print(
            "Assinatura digital: encontrada"
        )
    print(
        "\nLote passou nas verificações estruturais."
    )

    return True