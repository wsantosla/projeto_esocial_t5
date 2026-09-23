from app.database.local.connection import SessionLocal
from app.database.local.models import EsocialDesligamento
from app.esocial.client.lote import gerar_lote_eventos
from app.esocial.client.soap import criar_envelope_soap
from app.esocial.client.enviar import enviar_soap

def testar_envio():
    session=SessionLocal()
    try:
        evento=(
            session.query(EsocialDesligamento)
            .filter(
                EsocialDesligamento.xml.is_not(None),
                EsocialDesligamento.id_evento.is_not(None),
            )
            .first()
        )

        if not evento:
            print('Nenhum evento encotrado.')
            return
        print("Matricula:",evento.matricula)
        print("Id",evento.id_evento)
        #Gera Lote
        lote=gerar_lote_eventos(evento)
        #Gera SOAP
        soap=criar_envelope_soap(lote)    
        print("\nSOAP preparado")

        #Envia
        resposta =enviar_soap(soap)

        print("\nEnvio concluido.")
    finally:
        session.close()

if __name__ == "__main__":
    testar_envio()