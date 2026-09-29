from app.etl.extract.desligamento import extract
from app.etl.load.desligamento import load

df = extract()

print(f"Qtd de Registros:{len(df)}")

load(df)