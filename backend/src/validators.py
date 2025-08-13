from pydantic import BaseModel, validator, Field
from typing import Optional
from .constants import MIN_LIMIT, MAX_LIMIT, MIN_DAYS, MAX_DAYS, Currency

class CryptoPricesRequest(BaseModel):
    """Валидация запроса цен криптовалют"""
    limit: int = Field(default=100, ge=MIN_LIMIT, le=MAX_LIMIT, description="Количество монет")
    convert: Currency = Field(default=Currency.USD, description="Валюта конвертации")
    
    @validator('limit')
    def validate_limit(cls, v):
        if v < MIN_LIMIT or v > MAX_LIMIT:
            raise ValueError(f'Лимит должен быть от {MIN_LIMIT} до {MAX_LIMIT}')
        return v

class TechnicalAnalysisRequest(BaseModel):
    """Валидация запроса технического анализа"""
    coin_id: str = Field(..., min_length=1, max_length=10, description="ID или символ монеты")
    days: int = Field(default=30, ge=MIN_DAYS, le=MAX_DAYS, description="Количество дней для анализа")
    
    @validator('coin_id')
    def validate_coin_id(cls, v):
        if not v.isalnum():
            raise ValueError('ID монеты должен содержать только буквы и цифры')
        return v.upper()
    
    @validator('days')
    def validate_days(cls, v):
        if v < MIN_DAYS or v > MAX_DAYS:
            raise ValueError(f'Количество дней должно быть от {MIN_DAYS} до {MAX_DAYS}')
        return v

class SearchRequest(BaseModel):
    """Валидация запроса поиска"""
    query: str = Field(..., min_length=1, max_length=50, description="Поисковый запрос")
    
    @validator('query')
    def validate_query(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Поисковый запрос не может быть пустым')
        return v.strip()

class PriceHistoryRequest(BaseModel):
    """Валидация запроса истории цен"""
    coin_id: str = Field(..., min_length=1, max_length=10, description="ID или символ монеты")
    days: int = Field(default=30, ge=MIN_DAYS, le=MAX_DAYS, description="Количество дней")
    
    @validator('coin_id')
    def validate_coin_id(cls, v):
        if not v.isalnum():
            raise ValueError('ID монеты должен содержать только буквы и цифры')
        return v.upper()

def validate_api_key(api_key: Optional[str]) -> bool:
    """Проверка наличия API ключа"""
    if not api_key or api_key == "your_api_key_here":
        return False
    return True

def validate_positive_number(value: float, field_name: str) -> float:
    """Проверка положительного числа"""
    if value < 0:
        raise ValueError(f'{field_name} не может быть отрицательным')
    return value

def validate_percentage(value: float, field_name: str) -> float:
    """Проверка процентного значения"""
    if value < -100 or value > 1000:  # Допускаем большие проценты для криптовалют
        raise ValueError(f'{field_name} должен быть в диапазоне от -100 до 1000')
    return value 