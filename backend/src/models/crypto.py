from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from ..constants import Currency

class CryptoPrice(BaseModel):
    """Модель цены криптовалюты"""
    id: int = Field(..., description="ID монеты")
    name: str = Field(..., description="Название монеты")
    symbol: str = Field(..., description="Символ монеты")
    price: float = Field(..., description="Текущая цена")
    market_cap: float = Field(..., description="Рыночная капитализация")
    volume_24h: float = Field(..., description="Объем торгов за 24 часа")
    change_24h: float = Field(..., description="Изменение цены за 24 часа в %")
    last_updated: str = Field(..., description="Время последнего обновления")

class CoinInfo(BaseModel):
    """Модель информации о монете"""
    id: int = Field(..., description="ID монеты")
    name: str = Field(..., description="Название монеты")
    symbol: str = Field(..., description="Символ монеты")
    slug: str = Field(..., description="Slug монеты")
    price: float = Field(..., description="Текущая цена")
    market_cap: float = Field(..., description="Рыночная капитализация")
    volume_24h: float = Field(..., description="Объем торгов за 24 часа")
    change_1h: float = Field(..., description="Изменение цены за 1 час в %")
    change_24h: float = Field(..., description="Изменение цены за 24 часа в %")
    change_7d: float = Field(..., description="Изменение цены за 7 дней в %")
    circulating_supply: Optional[float] = Field(None, description="Обращающееся предложение")
    total_supply: Optional[float] = Field(None, description="Общее предложение")
    max_supply: Optional[float] = Field(None, description="Максимальное предложение")
    cmc_rank: Optional[int] = Field(None, description="Ранг по CoinMarketCap")
    last_updated: str = Field(..., description="Время последнего обновления")
    tags: List[str] = Field(default=[], description="Теги монеты")
    platform: Optional[Dict[str, Any]] = Field(None, description="Информация о платформе")
    description: Optional[str] = Field(None, description="Описание монеты")

class SearchResult(BaseModel):
    """Модель результата поиска"""
    id: int = Field(..., description="ID монеты")
    name: str = Field(..., description="Название монеты")
    symbol: str = Field(..., description="Символ монеты")
    slug: str = Field(..., description="Slug монеты")
    rank: Optional[int] = Field(None, description="Ранг монеты")
    is_active: bool = Field(..., description="Активна ли монета")
    first_historical_data: Optional[str] = Field(None, description="Дата первых исторических данных")
    last_historical_data: Optional[str] = Field(None, description="Дата последних исторических данных")

class TrendingCoin(BaseModel):
    """Модель трендовой монеты"""
    id: int = Field(..., description="ID монеты")
    name: str = Field(..., description="Название монеты")
    symbol: str = Field(..., description="Символ монеты")
    price: float = Field(..., description="Текущая цена")
    change_24h: float = Field(..., description="Изменение цены за 24 часа в %")
    volume_24h: float = Field(..., description="Объем торгов за 24 часа")
    market_cap: float = Field(..., description="Рыночная капитализация")

class HistoricalData(BaseModel):
    """Модель исторических данных"""
    timestamp: str = Field(..., description="Временная метка")
    price: float = Field(..., description="Цена")
    volume: float = Field(..., description="Объем торгов")
    market_cap: float = Field(..., description="Рыночная капитализация") 