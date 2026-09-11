from datetime import datetime
from app.config.esocial import ESOCIAL_TP_INSC,ESOCIAL_NR_INSC
from app.esocial.xml.controle_id import obter_sequencial

def gerar_id_evento():

    nr_incricao=ESOCIAL_NR_INSC.ljust(14,"0")
    agora =datetime.now()
    sequencial=obter_sequencial()
    id_evento = ("ID"
                 +ESOCIAL_TP_INSC
                 +nr_incricao+agora.strftime("%Y%m%d%H%M%S")
                 +f"{sequencial:05d}"
    )
    if len(id_evento) != 36:
        raise ValueError(f"Id do invalido:{id_evento}" 
                          f"possui {len(id_evento)}")

    return id_evento
if __name__ == "__main__":

    id_evento = gerar_id_evento()

    print(id_evento)
    print(len(id_evento))