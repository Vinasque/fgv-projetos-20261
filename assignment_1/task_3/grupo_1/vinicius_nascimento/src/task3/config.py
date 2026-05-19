from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    aws_region: str
    glue_database: str
    data_s3_base_path: str
    athena_s3_output: str

    @property
    def normalized_data_s3_base_path(self) -> str:
        return self.data_s3_base_path.rstrip("/")


def get_settings() -> Settings:
    missing = []

    aws_region = os.getenv("AWS_REGION", "").strip()
    glue_database = os.getenv("GLUE_DATABASE", "").strip()
    data_s3_base_path = os.getenv("DATA_S3_BASE_PATH", "").strip()
    athena_s3_output = os.getenv("ATHENA_S3_OUTPUT", "").strip()

    for name, value in {
        "AWS_REGION": aws_region,
        "GLUE_DATABASE": glue_database,
        "DATA_S3_BASE_PATH": data_s3_base_path,
        "ATHENA_S3_OUTPUT": athena_s3_output,
    }.items():
        if not value:
            missing.append(name)

    if missing:
        raise ValueError(
            "Variáveis de ambiente ausentes: "
            + ", ".join(missing)
            + ". Configure o arquivo .env ou exporte as variáveis no terminal."
        )

    return Settings(
        aws_region=aws_region,
        glue_database=glue_database,
        data_s3_base_path=data_s3_base_path,
        athena_s3_output=athena_s3_output,
    )
