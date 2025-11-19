from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"
PARQUET_PATH = DATA_PROCESSED / "base_chamados_skillmind.parquet"
