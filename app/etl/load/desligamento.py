from app.database.local.connection import SessionLocal
from app.database.local.models import StgDesligamento

def load(df):
    session = SessionLocal()

    try:

        novos = 0
        existentes =0

        for _, row in df.iterrows():

            registro_existente = (
                session.query(StgDesligamento)
                .filter(
                    StgDesligamento.matricula == row["matricula"]
                )
                .first()
            
            )
            if registro_existente:
                existentes += 1
                continue

            registro = StgDesligamento(
            matricula=row["matricula"],
            cpf = row["cpf"],
            data_afastamento=row["data_afastamento"],
            codigo_pmjp = row["codigo_pmjp"],
            descricao=row["descricao"],
            codigo_esocial=row["codigo_esocial"],
            )

            session.add(registro)
            novos +=1
        session.commit()

        print(f"Novos:{novos}")
        print(f"Registros ja existentes:{existentes}")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
