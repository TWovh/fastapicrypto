from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Dict, Any
from ..services.crypto_service import CryptoService
from ..dependencies import CoinMarketCapClientDep, TechnicalAnalyzerDep
from ..coinmarketcap_client import CoinMarketCapClient
from ..technical_analysis import TechnicalAnalyzer
from ..models.technical import TechnicalAnalysis
from ..validators import TechnicalAnalysisRequest
from ..constants import DEFAULT_DAYS, MIN_DAYS, MAX_DAYS
from ..exceptions import InsufficientDataError, raise_http_exception
from loguru import logger

router = APIRouter(
    prefix="/technical",
    tags=["technical-analysis"],
    responses={404: {"description": "Not found"}},
)

@router.get("/analyze/{coin_id}", response_model=TechnicalAnalysis)
async def analyze_coin(
    coin_id: str,
    days: int = Query(DEFAULT_DAYS, ge=MIN_DAYS, le=MAX_DAYS, description="Количество дней для анализа"),
    client: CoinMarketCapClient = CoinMarketCapClientDep,
    analyzer: TechnicalAnalyzer = TechnicalAnalyzerDep
):
    """
    Технический анализ криптовалюты
    
    - **coin_id**: ID или символ монеты
    - **days**: Количество дней для анализа (1-365)
    """
    try:
        # Получаем исторические данные
        service = CryptoService(client)
        historical_data = await service.get_historical_data(coin_id, days)
        
        # Проверяем достаточность данных
        if len(historical_data) < 20:
            raise InsufficientDataError(20, len(historical_data))
        
        # Выполняем технический анализ
        analysis_result = analyzer.analyze(historical_data)
        
        logger.info(f"Выполнен технический анализ для {coin_id} за {days} дней")
        return analysis_result
        
    except InsufficientDataError as e:
        logger.warning(f"Недостаточно данных для анализа {coin_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка технического анализа для {coin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/indicators/{coin_id}")
async def get_technical_indicators(
    coin_id: str,
    days: int = Query(DEFAULT_DAYS, ge=MIN_DAYS, le=MAX_DAYS, description="Количество дней"),
    client: CoinMarketCapClient = CoinMarketCapClientDep,
    analyzer: TechnicalAnalyzer = TechnicalAnalyzerDep
):
    """
    Получение технических индикаторов
    
    - **coin_id**: ID или символ монеты
    - **days**: Количество дней (1-365)
    """
    try:
        service = CryptoService(client)
        historical_data = await service.get_historical_data(coin_id, days)
        
        if len(historical_data) < 20:
            raise InsufficientDataError(20, len(historical_data))
        
        # Извлекаем цены
        prices = [item.get('price', 0) for item in historical_data]
        
        # Вычисляем индикаторы
        indicators = {
            "sma_20": analyzer.calculate_sma(prices, 20)[-1] if len(prices) >= 20 else None,
            "sma_50": analyzer.calculate_sma(prices, 50)[-1] if len(prices) >= 50 else None,
            "rsi": analyzer.calculate_rsi(prices, 14)[-1] if len(prices) >= 14 else None,
            "macd": analyzer.calculate_macd(prices),
            "bollinger_bands": analyzer.calculate_bollinger_bands(prices, 20)
        }
        
        logger.info(f"Получены технические индикаторы для {coin_id}")
        return {
            "coin_id": coin_id,
            "days": days,
            "indicators": indicators
        }
        
    except InsufficientDataError as e:
        logger.warning(f"Недостаточно данных для индикаторов {coin_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка получения индикаторов для {coin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trend/{coin_id}")
async def get_trend_analysis(
    coin_id: str,
    days: int = Query(DEFAULT_DAYS, ge=MIN_DAYS, le=MAX_DAYS, description="Количество дней"),
    client: CoinMarketCapClient = CoinMarketCapClientDep,
    analyzer: TechnicalAnalyzer = TechnicalAnalyzerDep
):
    """
    Анализ тренда криптовалюты
    
    - **coin_id**: ID или символ монеты
    - **days**: Количество дней (1-365)
    """
    try:
        service = CryptoService(client)
        historical_data = await service.get_historical_data(coin_id, days)
        
        if len(historical_data) < 20:
            raise InsufficientDataError(20, len(historical_data))
        
        # Извлекаем цены
        prices = [item.get('price', 0) for item in historical_data]
        
        # Анализируем тренд
        trend_analysis = analyzer.analyze_trend(prices)
        
        logger.info(f"Выполнен анализ тренда для {coin_id}")
        return {
            "coin_id": coin_id,
            "days": days,
            "trend_analysis": trend_analysis
        }
        
    except InsufficientDataError as e:
        logger.warning(f"Недостаточно данных для анализа тренда {coin_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка анализа тренда для {coin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 