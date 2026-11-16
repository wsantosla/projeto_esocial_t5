
from app.database.local.models import EsocialDesligamento

from app.esocial.xml.desligamento import (
    gerar_e_salvar_xml,
)

from app.esocial.signature.assinador import (
    assinar_xml,
    verificar_assinatura,
)

from app.esocial.signature.certificado import (
    carregar_certificado,
)

from app.esocial.validators.xsd_desligamento import (
    carregar_schema_desligamento,
    validar_xml_desligamento,
)
from app.esocial.xml.id_evento import gerar_id_evento

def processar_eventos(session):

    resultado = {
        "preparados": 0,
        "assinados": 0,
        "validos": 0,
        "erros": [],
    }

    # Carrega o certificado e o XSD uma única vez
    chave_privada, certificado, _ = carregar_certificado()
    schema = carregar_schema_desligamento()

    eventos = (
        session.query(EsocialDesligamento)
        .filter(
            EsocialDesligamento.id_evento.is_not(None),
            EsocialDesligamento.xml.is_(None),
        )
        .all()
    )

    for evento in eventos:

        try:
            if not evento.id:
                evento.id_evento = gerar_id_evento()
                session.flush()   
            # 1. Gerar XML
            gerar_e_salvar_xml(evento, session)
            session.flush()

            resultado["preparados"] += 1

            # 2. Assinar XML
            xml_assinado = assinar_xml(
                evento.xml.encode("UTF-8"),
                chave_privada,
                certificado,
            )

            # 3. Verificar assinatura
            verificar_assinatura(
                xml_assinado,
                certificado,
            )

            evento.xml = xml_assinado.decode("UTF-8")

            resultado["assinados"] += 1

            # 4. Validar XSD
            validar_xml_desligamento(
                xml_assinado,
                schema,
            )

            resultado["validos"] += 1

            session.commit()

        except Exception as erro:

            session.rollback()

            resultado["erros"].append({
                "matricula": evento.matricula,
                "id_evento": evento.id_evento,
                "erro": str(erro),
            })

    return resultado
