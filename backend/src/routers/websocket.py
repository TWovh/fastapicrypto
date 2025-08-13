from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, Any
from ..dependencies import WebSocketManagerDep, CoinMarketCapClientDep
from ..services.crypto_service import CryptoService
from ..coinmarketcap_client import CoinMarketCapClient
from ..websocket_manager import WebSocketManager
from loguru import logger

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
    responses={404: {"description": "Not found"}},
)

@router.websocket("/crypto/prices")
async def websocket_crypto_prices(
    websocket: WebSocket,
    ws_manager: WebSocketManager = WebSocketManagerDep,
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    WebSocket для получения цен криптовалют в реальном времени
    """
    await ws_manager.connect(websocket)
    
    try:
        service = CryptoService(client)
        
        while True:
            # Получаем актуальные цены
            prices = await service.get_crypto_prices(limit=10)  # Топ 10 монет
            
            # Отправляем данные клиенту
            await websocket.send_json({
                "type": "crypto_prices",
                "data": [price.dict() for price in prices],
                "timestamp": prices[0].last_updated if prices else None
            })
            
            # Ждем 30 секунд перед следующим обновлением
            import asyncio
            await asyncio.sleep(30)
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info("WebSocket соединение закрыто")
    except Exception as e:
        logger.error(f"Ошибка WebSocket: {e}")
        ws_manager.disconnect(websocket)

@router.websocket("/crypto/{coin_id}")
async def websocket_coin_data(
    websocket: WebSocket,
    coin_id: str,
    ws_manager: WebSocketManager = WebSocketManagerDep,
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    WebSocket для получения данных конкретной монеты
    """
    await ws_manager.connect(websocket)
    
    try:
        service = CryptoService(client)
        
        while True:
            # Получаем информацию о монете
            coin_info = await service.get_coin_info(coin_id)
            
            # Отправляем данные клиенту
            await websocket.send_json({
                "type": "coin_data",
                "coin_id": coin_id,
                "data": coin_info.dict(),
                "timestamp": coin_info.last_updated
            })
            
            # Ждем 10 секунд перед следующим обновлением
            import asyncio
            await asyncio.sleep(10)
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info(f"WebSocket соединение для {coin_id} закрыто")
    except Exception as e:
        logger.error(f"Ошибка WebSocket для {coin_id}: {e}")
        ws_manager.disconnect(websocket)

@router.websocket("/market/overview")
async def websocket_market_overview(
    websocket: WebSocket,
    ws_manager: WebSocketManager = WebSocketManagerDep,
    client: CoinMarketCapClient = CoinMarketCapClientDep
):
    """
    WebSocket для получения обзора рынка
    """
    await ws_manager.connect(websocket)
    
    try:
        service = CryptoService(client)
        
        while True:
            # Получаем трендовые монеты
            trending = await service.get_trending_coins()
            
            # Получаем топ монет
            top_coins = await service.get_crypto_prices(limit=20)
            
            # Формируем обзор рынка
            market_overview = {
                "trending_coins": [coin.dict() for coin in trending],
                "top_coins": [coin.dict() for coin in top_coins],
                "total_coins": len(top_coins),
                "timestamp": top_coins[0].last_updated if top_coins else None
            }
            
            # Отправляем данные клиенту
            await websocket.send_json({
                "type": "market_overview",
                "data": market_overview
            })
            
            # Ждем 60 секунд перед следующим обновлением
            import asyncio
            await asyncio.sleep(60)
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info("WebSocket соединение для обзора рынка закрыто")
    except Exception as e:
        logger.error(f"Ошибка WebSocket для обзора рынка: {e}")
        ws_manager.disconnect(websocket) 