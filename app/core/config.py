from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_USER: str = Field(...)
    DB_PASSWORD: str = Field(...)
    DB_HOST: str = Field(...)
    DB_PORT: int = Field(default=3306)
    DB_NAME: str = Field(...)
    DB_ECHO: bool = Field(default=False)
    API_PREFIX: str = Field(default="/api")

    @property
    def sqlalchemy_database_uri(self) -> str:
        # Usamos PyMySQL como driver
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
