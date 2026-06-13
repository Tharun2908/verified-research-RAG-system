from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres
    postgres_user: str = "research"
    postgres_password: str = "research"
    postgres_db: str = "research"
    postgres_host: str = "localhost"
    postgres_port: int = 15432

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 16379

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 16333

    # tells pydantic-settings to read from a .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> str:
        # async driver URL that SQLAlchemy + asyncpg expect
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    # LLM generation (swappable backend)
    llm_base_url: str = "stub"          # "stub" = local fake; otherwise an OpenAI-compatible URL
    llm_api_key: str = "not-needed"     # real key only for hosted APIs
    llm_model: str = "mistral-7b"       # model name passed to the server


settings = Settings()