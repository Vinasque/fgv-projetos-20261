from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from task3.athena import create_glue_database, create_all_external_tables, validate_tables


if __name__ == "__main__":
    create_glue_database()
    create_all_external_tables()
    df = validate_tables()
    print("\nValidação das tabelas:")
    print(df.to_string(index=False))
