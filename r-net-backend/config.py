import os
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4-vision-preview")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "4096"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Server Configuration
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # File Upload Settings
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "5242880"))  # 5MB
    allowed_extensions: str = os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif,webp")
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "./logs/app.log")
    
    # Rate Limiting
    rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "5"))
    
    # Caching
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    cache_max_size: int = int(os.getenv("CACHE_MAX_SIZE", "100"))
    
    # Security
    require_api_key: bool = os.getenv("REQUIRE_API_KEY", "False").lower() == "true"
    api_keys: str = os.getenv("API_KEYS", "")  # Comma-separated list
    
    @property
    def allowed_extensions_list(self) -> list:
        return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]
    
    @property
    def api_keys_list(self) -> list:
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()

# Configure logging
def setup_logging():
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

setup_logging()
logger = logging.getLogger(__name__)