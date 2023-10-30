from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url: str = "https://www.google.com/"
    database_host: str = "127.0.0.1"
    database_user: str = "postgres"
    database_password: str = "S3cret"
    database_name: str = "postgres"
    database_port: int = 5432

    database_dsn: str = ""

    @field_validator("database_dsn", mode="before")
    def make_dsn(cls, v: str, info: ValidationInfo) -> str:
        """Make postgres dsn"""
        return v or (
            f"postgresql://{info.data['database_user']}:{info.data['database_password']}@"
            f"{info.data['database_host']}:{info.data['database_port']}/{info.data['database_name']}"
        )