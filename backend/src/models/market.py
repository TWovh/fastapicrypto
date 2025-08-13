from pydantic import BaseModel, Field
from typing import Dict, Optional

class MarketData(BaseModel):
    """Модель рыночных данных"""
    total_market_cap: float = Field(..., description="Общая рыночная капитализация")
    total_volume_24h: float = Field(..., description="Общий объем торгов за 24 часа")
    market_cap_percentage: Dict[str, float] = Field(..., description="Процентное распределение по монетам")
    market_cap_change_24h: float = Field(..., description="Изменение рыночной капитализации за 24 часа")
    active_cryptocurrencies: int = Field(..., description="Количество активных криптовалют")
    total_cryptocurrencies: int = Field(..., description="Общее количество криптовалют")
    active_market_pairs: int = Field(..., description="Количество активных торговых пар")
    last_updated: str = Field(..., description="Время последнего обновления")

class MarketOverview(BaseModel):
    """Модель обзора рынка"""
    market_data: MarketData = Field(..., description="Рыночные данные")
    top_gainers: list = Field(..., description="Топ растущих монет")
    top_losers: list = Field(..., description="Топ падающих монет")
    trending_coins: list = Field(..., description="Трендовые монеты") 