from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "On-Device LLM Assistant PoC"
    app_env: str = "dev"
    app_port: int = 8000

    mariadb_host: str = "127.0.0.1"
    mariadb_port: int = 3306
    mariadb_user: str = "root"
    mariadb_password: str = "changeme"
    mariadb_database: str = "poc_llm"
    enable_mariadb: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
