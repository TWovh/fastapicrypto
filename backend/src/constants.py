from enum import Enum
from typing import List

class Currency(str, Enum):
    """Поддерживаемые валюты"""
    USD = "USD"
    EUR = "EUR"
    BTC = "BTC"
    ETH = "ETH"

class Timeframe(str, Enum):
    """Временные интервалы для анализа"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class SortOrder(str, Enum):
    """Порядок сортировки"""
    ASC = "asc"
    DESC = "desc"

class SortField(str, Enum):
    """Поля для сортировки"""
    PRICE = "price"
    MARKET_CAP = "market_cap"
    VOLUME = "volume_24h"
    CHANGE_24H = "percent_change_24h"

# Константы для API
DEFAULT_LIMIT = 100
MAX_LIMIT = 5000
MIN_LIMIT = 1

DEFAULT_DAYS = 30
MAX_DAYS = 365
MIN_DAYS = 1

# Константы для технического анализа
DEFAULT_RSI_PERIOD = 14
DEFAULT_SMA_PERIOD = 20
DEFAULT_EMA_PERIOD = 12
DEFAULT_MACD_FAST = 12
DEFAULT_MACD_SLOW = 26
DEFAULT_MACD_SIGNAL = 9

# Сообщения об ошибках
ERROR_MESSAGES = {
    "api_key_missing": "API ключ CoinMarketCap не настроен",
    "coin_not_found": "Монета не найдена",
    "insufficient_data": "Недостаточно данных для анализа",
    "invalid_limit": f"Лимит должен быть от {MIN_LIMIT} до {MAX_LIMIT}",
    "invalid_days": f"Количество дней должно быть от {MIN_DAYS} до {MAX_DAYS}",
    "service_unavailable": "Сервис временно недоступен"
} 