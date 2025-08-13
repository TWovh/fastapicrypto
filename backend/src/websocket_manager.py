"""
WebSocket Manager
Менеджер для управления WebSocket соединениями
"""

import json
import asyncio
from typing import List, Dict, Any
from fastapi import WebSocket
from loguru import logger

class WebSocketManager:
    """Менеджер WebSocket соединений"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_count = 0
    
    async def connect(self, websocket: WebSocket):
        """Подключение нового клиента"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_count += 1
        
        logger.info(f"🔌 WebSocket подключен. Всего соединений: {self.connection_count}")
        
        # Отправляем приветственное сообщение
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "message": "Подключение к Crypto Analytics API установлено",
            "timestamp": asyncio.get_event_loop().time()
        }))
    
    def disconnect(self, websocket: WebSocket):
        """Отключение клиента"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.connection_count -= 1
            logger.info(f"🔌 WebSocket отключен. Всего соединений: {self.connection_count}")
    
    async def send_data(self, data: Dict[str, Any]):
        """Отправка данных всем подключенным клиентам"""
        if not self.active_connections:
            return
        
        message = json.dumps(data)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Ошибка отправки WebSocket сообщения: {e}")
                disconnected.append(connection)
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Отправка персонального сообщения"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Ошибка отправки персонального сообщения: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        """Широковещательная отправка сообщения"""
        if not self.active_connections:
            return
        
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Ошибка широковещательной отправки: {e}")
                disconnected.append(connection)
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection)
    
    def get_connection_count(self) -> int:
        """Получение количества активных соединений"""
        return self.connection_count
    
    async def send_price_update(self, prices: List[Dict[str, Any]]):
        """Отправка обновления цен"""
        await self.send_data({
            "type": "price_update",
            "data": prices,
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def send_market_update(self, market_data: Dict[str, Any]):
        """Отправка обновления рыночных данных"""
        await self.send_data({
            "type": "market_update",
            "data": market_data,
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def send_alert(self, alert_type: str, message: str, data: Dict[str, Any] = None):
        """Отправка алерта"""
        alert_data = {
            "type": "alert",
            "alert_type": alert_type,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        if data:
            alert_data["data"] = data
        
        await self.send_data(alert_data) 