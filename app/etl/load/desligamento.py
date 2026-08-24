from app.database.local.connection import SessionLocal
from app.database.local.models import StgDesligamento

def load(df):
    session = SessionLocal()

    try:

        novos = 0
        existentes =0

        for _, in df.iterrows():

            registro_existente = (
                session.query(StgDesligamento).filter(
                    StgDesligamento.matricula == row["matricula"])).first()
            
            )