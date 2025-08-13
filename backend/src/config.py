from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API ключи
    coinmarketcap_api_key: str
    
    # Настройки сервера
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Настройки логирования
    log_level: str = "INFO"
    log_file: str = "logs/api.log"
    
    # Настройки API
    api_title: str = "Crypto Analytics API"
    api_description: str = "API для аналитики криптовалют с данными от CoinMarketCap"
    api_version: str = "2.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Создаем глобальный экземпляр настроек
settings = Settings() 