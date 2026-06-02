from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    openai_structured_output_model: str = "gpt-4.1"
    azure_openai_api_version: str = "2024-12-01-preview"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
