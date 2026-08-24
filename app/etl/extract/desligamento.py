import pandas as pd

from app.database.source.connection import engine_source
from app.database.source.queries import QUERY_DESLIGAMENTO


def extract():

    with engine_source.connect() as conn:
        df = pd.read_sql(
            QUERY_DESLIGAMENTO,
            conn
        )
    return df

if __name__=="__main__":
    df = extract()
    print(df.columns.tolist())
    print()
    print(df.dtypes)
    