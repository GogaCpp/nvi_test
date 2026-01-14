from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    # Postgres
    db_user: str = Field(alias="POSTGRES_USER")
    db_password: str = Field(alias="POSTGRES_PASSWORD")
    db_name: str = Field(alias="POSTGRES_DB")
    db_host: str = Field(alias="POSTGRES_HOST")
    db_port: int = Field(alias="POSTGRES_PORT")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8"
)
