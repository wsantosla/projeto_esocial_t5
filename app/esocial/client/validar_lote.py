
from lxml import etree


NS_SIGNATURE = "http://www.w3.org/2000/09/xmldsig#"


def validar_lote(xml_lote):

    raiz = etree.fromstring(xml_lote)

    if etree.QName(raiz).localname != "eSocial":
        raise ValueError("Raiz do lote não é eSocial.")

    envio = raiz.find(".//{*}envioLoteEventos")

    if envio is None:
        raise ValueError("envioLoteEventos não encontrado.")

    grupo = envio.get("grupo")

    if grupo != "2":
        raise ValueError(f"Grupo inválido: {grupo}")

    eventos = envio.find("{*}eventos")

    if eventos is None:
        raise ValueError("Grupo eventos não encontrado.")

    lista_eventos = eventos.findall("{*}evento")

    if not lista_eventos:
        raise ValueError("Nenhum evento encontrado no lote.")

    print(f"Eventos encontrados: {len(lista_eventos)}")

    for evento in lista_eventos:

        id_lote = evento.get("Id")

        xml_evento = evento.find("{*}eSocial")

        if xml_evento is None:
            raise ValueError("XML do evento não encontrado.")

        # Identifica o elemento do evento sem fixar S-2299.
        elementos_evento = [
            elemento
            for elemento in xml_evento
            if etree.QName(elemento).localname.startswith("evt")
        ]

        if len(elementos_evento) != 1:
            raise ValueError(
                "Não foi possível identificar um único evento."
            )

        elemento_evento = elementos_evento[0]
        id_evt = elemento_evento.get("Id")

        print("Tipo de evento:", etree.QName(elemento_evento).localname)
        print("Id do evento:", id_evt)

        if id_lote != id_evt:
            raise ValueError(
                "Os Ids do lote e do evento são diferentes."
            )

        assinatura = xml_evento.find(
            f"{{{NS_SIGNATURE}}}Signature"
        )

        if assinatura is None:
            raise ValueError("Assinatura digital não encontrada.")

        print("Assinatura digital: encontrada")

    print("\nLote passou nas verificações estruturais.")

    return True
