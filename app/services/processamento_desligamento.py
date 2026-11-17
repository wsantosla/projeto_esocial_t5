
from lxml import etree

from app.database.local.models import EsocialDesligamento

from app.esocial.xml.desligamento import gerar_e_salvar_xml
from app.esocial.xml.id_evento import gerar_id_evento

from app.esocial.signature.assinador import (
    assinar_xml,
    verificar_assinatura,
)

from app.esocial.signature.certificado import carregar_certificado

from app.esocial.validators.xsd_desligamento import (
    carregar_schema_desligamento,
    validar_xml_desligamento,
)


def processar_eventos(session):

    resultado = {
        "preparados": 0,
        "assinados": 0,
        "validos": 0,
        "erros": [],
    }

    # Carrega certificado e XSD uma única vez
    chave_privada, certificado, _ = carregar_certificado()
    schema = carregar_schema_desligamento()

    # Busca todos os eventos
    eventos = (
        session.query(EsocialDesligamento)
        .order_by(EsocialDesligamento.id)
        .all()
    )

    for evento in eventos:

        matricula = evento.matricula
        id_evento = evento.id_evento

        preparado = False
        assinado = False

        try:

            # 1. Gerar ID, se estiver faltando
            if not evento.id_evento:

                if evento.xml:
                    raise ValueError(
                        "Registro possui XML, mas não possui ID do evento."
                    )

                evento.id_evento = gerar_id_evento()
                session.flush()

            # 2. Gerar XML somente se ainda não existir
            if not evento.xml:

                gerar_e_salvar_xml(evento, session)
                session.flush()

                preparado = True

            xml = evento.xml.encode("UTF-8")

            # 3. Verificar se já existe assinatura
            raiz = etree.fromstring(xml)

            assinaturas = raiz.xpath(
                ".//*[local-name()='Signature']"
            )

            if len(assinaturas) > 1:
                raise ValueError(
                    "XML possui mais de uma assinatura digital."
                )

            # 4. Assinar somente se ainda não estiver assinado
            if len(assinaturas) == 0:

                xml = assinar_xml(
                    xml,
                    chave_privada,
                    certificado,
                )

                evento.xml = xml.decode("UTF-8")
                assinado = True

            # 5. Verificar assinatura digital
            verificar_assinatura(
                xml,
                certificado,
            )

            # 6. Validar XML assinado no XSD
            validar_xml_desligamento(
                xml,
                schema,
            )

            # 7. Salvar no banco
            session.commit()

            # Atualizar indicadores somente após commit
            if preparado:
                resultado["preparados"] += 1

            if assinado:
                resultado["assinados"] += 1

            resultado["validos"] += 1

        except Exception as erro:

            session.rollback()

            resultado["erros"].append({
                "matricula": matricula,
                "id_evento": id_evento,
                "erro": str(erro),
            })

    return resultado
