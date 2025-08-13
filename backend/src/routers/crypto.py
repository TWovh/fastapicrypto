from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from ..services.crypto_service import CryptoService
from ..dependencies import CoinMarketCapClientDep
from ..coinmarketcap_client import CoinMarketCapClient
from ..models.crypto import CryptoPrice, CoinInfo, SearchResult, TrendingCoin
from ..validators import CryptoPricesRequest, SearchRequest
from ..constants import Currency, DEFAULT_LIMIT, MIN_LIMIT, MAX_LIMIT
from ..exceptions import raise_http_exception
from loguru import logger

# Создаем роутер с префиксом и тегами
router = APIRouter(
    prefix="/crypto",
    tags=["cryptocurrencies"],
    responses={404: {"description": "Not found"}},
)

@router.get("/prices", response_model=List[CryptoPrice])
async def get_crypto_prices(
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT, description="Количество монет"),
    convert: Currency = Query(Currency.USD, description="Валюта конвертации"),
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    Получение цен криптовалют
    
    - **limit**: Количество монет (1-5000)
    - **convert**: Валюта конвертации (USD, EUR, BTC, ETH)
    """
    try:
        # Создаем сервис с клиентом
        service = CryptoService(client)
        
        # Получаем данные через сервис
        prices = await service.get_crypto_prices(limit, convert)
        
        logger.info(f"Запрошены цены {len(prices)} криптовалют")
        return prices
        
    except Exception as e:
        logger.error(f"Ошибка получения цен криптовалют: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{coin_id}", response_model=CoinInfo)
async def get_coin_info(
    coin_id: str,
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    Получение информации о конкретной монете
    
    - **coin_id**: ID или символ монеты (например: BTC, 1, bitcoin)
    """
    try:
        service = CryptoService(client)
        coin_info = await service.get_coin_info(coin_id)
        return coin_info
        
    except Exception as e:
        logger.error(f"Ошибка получения информации о монете {coin_id}: {e}")
        raise HTTPException(status_code=404, detail=f"Монета {coin_id} не найдена")

@router.get("/search/{query}", response_model=List[SearchResult])
async def search_cryptocurrencies(
    query: str,
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    Поиск криптовалют по названию или символу
    
    - **query**: Поисковый запрос
    """
    try:
        service = CryptoService(client)
        results = await service.search_cryptocurrencies(query)
        return results
        
    except Exception as e:
        logger.error(f"Ошибка поиска криптовалют '{query}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending/coins", response_model=List[TrendingCoin])
async def get_trending_coins(
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    Получение трендовых криптовалют
    """
    try:
        service = CryptoService(client)
        trending = await service.get_trending_coins()
        return trending
        
    except Exception as e:
        logger.error(f"Ошибка получения трендовых монет: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{coin_id}/history")
async def get_coin_history(
    coin_id: str,
    days: int = Query(30, ge=1, le=365, description="Количество дней"),
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    Получение исторических данных монеты
    
    - **coin_id**: ID или символ монеты
    - **days**: Количество дней (1-365)
    """
    try:
        service = CryptoService(client)
        history = await service.get_historical_data(coin_id, days)
        return {
            "coin_id": coin_id,
            "days": days,
            "data": history
        }
        
    except Exception as e:
        logger.error(f"Ошибка получения истории для {coin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 