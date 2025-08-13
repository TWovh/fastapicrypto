from fastapi import Depends
from typing import Optional
from .coinmarketcap_client import CoinMarketCapClient
from .websocket_manager import WebSocketManager
from .technical_analysis import TechnicalAnalyzer
from .config import settings
from .exceptions import APIKeyMissingError
from .validators import validate_api_key

# Глобальные экземпляры (создаются один раз при запуске)
_coinmarketcap_client: Optional[CoinMarketCapClient] = None
_websocket_manager: Optional[WebSocketManager] = None
_technical_analyzer: Optional[TechnicalAnalyzer] = None

def get_coinmarketcap_client() -> CoinMarketCapClient:
    """
    Dependency для получения клиента CoinMarketCap API
    
    Как работает Dependency Injection:
    1. FastAPI вызывает эту функцию при каждом запросе
    2. Функция возвращает готовый объект клиента
    3. FastAPI автоматически передает этот объект в эндпоинт
    4. Если объект еще не создан, создает его
    5. Если объект уже существует, возвращает существующий
    """
    global _coinmarketcap_client
    
    if _coinmarketcap_client is None:
        # Проверяем API ключ
        if not validate_api_key(settings.coinmarketcap_api_key):
            raise APIKeyMissingError()
        
        # Создаем клиент
        _coinmarketcap_client = CoinMarketCapClient()
    
    return _coinmarketcap_client

def get_websocket_manager() -> WebSocketManager:
    """
    Dependency для получения менеджера WebSocket соединений
    """
    global _websocket_manager
    
    if _websocket_manager is None:
        _websocket_manager = WebSocketManager()
    
    return _websocket_manager

def get_technical_analyzer() -> TechnicalAnalyzer:
    """
    Dependency для получения анализатора технических индикаторов
    """
    global _technical_analyzer
    
    if _technical_analyzer is None:
        _technical_analyzer = TechnicalAnalyzer()
    
    return _technical_analyzer

# Типизированные зависимости для лучшей поддержки IDE
CoinMarketCapClientDep = Depends(get_coinmarketcap_client)
WebSocketManagerDep = Depends(get_websocket_manager)
TechnicalAnalyzerDep = Depends(get_technical_analyzer)

# Пример использования в роутере:
# @router.get("/prices")
# async def get_prices(
#     client: CoinMarketCapClient = CoinMarketCapClientDep
# ):
#     return await client.get_crypto_prices() 