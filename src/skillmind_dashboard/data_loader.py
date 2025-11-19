import pandas as pd
from .config import PARQUET_PATH

def load_base():
    df = pd.read_parquet(PARQUET_PATH)

    # Convertendo datas — ajuste se necessário
    date_cols = [
        "Data de abertura",
        "Data da solução",
        "Data de fechamento"
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df
