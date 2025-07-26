from pydantic_settings import BaseSettings
from typing import List
from .models import ConfigurableField


class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # File upload settings
    max_file_size_mb: int = 10
    allowed_extensions: str = "pdf"  # Changed from List[str] to str

    class Config:
        env_file = ".env"

    @property
    def allowed_extensions_list(self) -> List[str]:
        """Convert allowed_extensions string to list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]


# Default configurable fields that are commonly extracted from documents
DEFAULT_CONFIGURABLE_FIELDS = [
    ConfigurableField(
        name="document_type",
        description="Type of document (e.g., invoice, contract, resume, etc.)",
        data_type="string"
    ),
    ConfigurableField(
        name="date",
        description="Primary date mentioned in the document",
        data_type="date"
    ),
    ConfigurableField(
        name="company_name",
        description="Company or organization name",
        data_type="string"
    ),
    ConfigurableField(
        name="person_name",
        description="Person's name (if applicable)",
        data_type="string"
    ),
    ConfigurableField(
        name="email",
        description="Email address",
        data_type="string"
    ),
    ConfigurableField(
        name="phone",
        description="Phone number",
        data_type="string"
    ),
    ConfigurableField(
        name="amount",
        description="Monetary amount (if applicable)",
        data_type="number"
    ),
    ConfigurableField(
        name="address",
        description="Physical address",
        data_type="string"
    ),
]

settings = Settings()
