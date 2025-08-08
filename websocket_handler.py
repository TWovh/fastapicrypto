import asyncio
import json
import websockets
import httpx
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: Dict[WebSocket, Set[str]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        self.subscriptions[websocket] = set()
        logger.info(f"Новое WebSocket соединение. Всего соединений: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]
        logger.info(f"WebSocket соединение закрыто. Осталось соединений: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Ошибка broadcast: {e}")
                disconnected.add(connection)
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection)

    def subscribe_to_coin(self, websocket: WebSocket, coin_symbol: str):
        """Подписка на обновления конкретной монеты"""
        if websocket in self.subscriptions:
            self.subscriptions[websocket].add(coin_symbol.upper())
            logger.info(f"Подписка на {coin_symbol.upper()} для соединения")

    def unsubscribe_from_coin(self, websocket: WebSocket, coin_symbol: str):
        """Отписка от обновлений конкретной монеты"""
        if websocket in self.subscriptions:
            self.subscriptions[websocket].discard(coin_symbol.upper())
            logger.info(f"Отписка от {coin_symbol.upper()} для соединения")

class CryptoWebSocketHandler:
    def __init__(self):
        self.manager = ConnectionManager()
        self.price_cache: Dict[str, float] = {}
        self.is_running = False

    async def handle_websocket(self, websocket: WebSocket):
        await self.manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await self.handle_message(websocket, data)
        except WebSocketDisconnect:
            self.manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"Ошибка WebSocket: {e}")
            self.manager.disconnect(websocket)

    async def handle_message(self, websocket: WebSocket, message: str):
        """Обработка входящих сообщений от клиента"""
        try:
            data = json.loads(message)
            action = data.get("action")
            
            if action == "subscribe":
                coin_symbol = data.get("coin", "").upper()
                if coin_symbol:
                    self.manager.subscribe_to_coin(websocket, coin_symbol)
                    await self.manager.send_personal_message(
                        json.dumps({
                            "type": "subscription",
                            "status": "success",
                            "coin": coin_symbol
                        }),
                        websocket
                    )
            
            elif action == "unsubscribe":
                coin_symbol = data.get("coin", "").upper()
                if coin_symbol:
                    self.manager.unsubscribe_from_coin(websocket, coin_symbol)
                    await self.manager.send_personal_message(
                        json.dumps({
                            "type": "unsubscription",
                            "status": "success",
                            "coin": coin_symbol
                        }),
                        websocket
                    )
            
            elif action == "get_prices":
                await self.manager.send_personal_message(
                    json.dumps({
                        "type": "prices",
                        "data": self.price_cache
                    }),
                    websocket
                )
            
            else:
                await self.manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Неизвестное действие"
                    }),
                    websocket
                )
                
        except json.JSONDecodeError:
            await self.manager.send_personal_message(
                json.dumps({
                    "type": "error",
                    "message": "Неверный формат JSON"
                }),
                websocket
            )
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {e}")
            await self.manager.send_personal_message(
                json.dumps({
                    "type": "error",
                    "message": "Внутренняя ошибка сервера"
                }),
                websocket
            )

    async def update_prices(self, prices: Dict[str, float]):
        """Обновление цен и отправка уведомлений подписчикам"""
        self.price_cache.update(prices)
        
        # Отправляем обновления подписчикам
        for websocket, subscriptions in self.manager.subscriptions.items():
            relevant_prices = {
                coin: price for coin, price in prices.items() 
                if coin in subscriptions
            }
            
            if relevant_prices:
                try:
                    await websocket.send_text(json.dumps({
                        "type": "price_update",
                        "data": relevant_prices,
                        "timestamp": asyncio.get_event_loop().time()
                    }))
                except Exception as e:
                    logger.error(f"Ошибка отправки обновления: {e}")
                    self.manager.disconnect(websocket)

    async def start_price_monitoring(self):
        """Запуск мониторинга цен с реальными данными"""
        self.is_running = True
        logger.info("Запуск мониторинга цен")
        
        while self.is_running:
            try:
                # Получаем реальные данные от CoinGecko
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "https://api.coingecko.com/api/v3/coins/markets",
                        params={
                            "vs_currency": "usd",
                            "order": "market_cap_desc",
                            "per_page": 20,
                            "page": 1,
                            "sparkline": False
                        }
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    # Обновляем кэш цен
                    prices = {}
                    for coin in data:
                        symbol = coin["symbol"].upper()
                        prices[symbol] = coin["current_price"]
                    
                    await self.update_prices(prices)
                    
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    logger.warning("Превышен лимит запросов к API. Попробуйте позже.")
                else:
                    logger.error(f"HTTP ошибка при получении данных: {e}")
                # Не обновляем цены при ошибке
            except Exception as e:
                logger.error(f"Ошибка при получении данных: {e}")
                # Не обновляем цены при ошибке
            
            await asyncio.sleep(60)  # Увеличиваем интервал до 60 секунд

    def stop_price_monitoring(self):
        """Остановка мониторинга цен"""
        self.is_running = False
        logger.info("Остановка мониторинга цен")

# Глобальный экземпляр обработчика
websocket_handler = CryptoWebSocketHandler() 