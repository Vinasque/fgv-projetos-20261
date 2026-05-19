from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from task3.athena import validate_tables


if __name__ == "__main__":
    df = validate_tables()
    print(df.to_string(index=False))
