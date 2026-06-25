from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./code_foundry.db"

    model_config = SettingsConfigDict(env_prefix="CODE_FOUNDRY_")


settings = Settings()

