"""Configuration from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    truenas_url: str = "wss://truenas.local/websocket"
    truenas_api_key: str
    truenas_verify_ssl: bool = False
    truenas_timeout: float = 30.0

    model_config = {"env_prefix": "", "env_file": ".env"}
