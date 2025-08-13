from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class TechnicalIndicators(BaseModel):
    """Модель технических индикаторов"""
    sma_20: Optional[float] = Field(None, description="Простая скользящая средняя за 20 периодов")
    sma_50: Optional[float] = Field(None, description="Простая скользящая средняя за 50 периодов")
    rsi: Optional[float] = Field(None, description="Индекс относительной силы")
    macd: Dict[str, Optional[float]] = Field(..., description="MACD индикатор")
    bollinger_bands: Dict[str, Optional[float]] = Field(..., description="Полосы Боллинджера")

class TrendAnalysis(BaseModel):
    """Модель анализа тренда"""
    trend: str = Field(..., description="Направление тренда")
    strength: str = Field(..., description="Сила тренда")
    price_change_percent: float = Field(..., description="Изменение цены в процентах")

class VolumeAnalysis(BaseModel):
    """Модель анализа объема"""
    volume_trend: str = Field(..., description="Тренд объема")
    price_volume_correlation: str = Field(..., description="Корреляция цены и объема")

class TechnicalAnalysis(BaseModel):
    """Модель технического анализа"""
    coin_id: str = Field(..., description="ID монеты")
    period_days: int = Field(..., description="Период анализа в днях")
    indicators: TechnicalIndicators = Field(..., description="Технические индикаторы")
    trend_analysis: TrendAnalysis = Field(..., description="Анализ тренда")
    volume_analysis: Optional[VolumeAnalysis] = Field(None, description="Анализ объема")
    support_resistance: Dict[str, List[float]] = Field(..., description="Уровни поддержки и сопротивления")

class PriceHistory(BaseModel):
    """Модель истории цен"""
    coin_id: str = Field(..., description="ID монеты")
    period_days: int = Field(..., description="Период в днях")
    data: List[Dict[str, float]] = Field(..., description="Исторические данные") 