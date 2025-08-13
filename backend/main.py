"""
FastAPI Crypto Analytics API - Entry Point
Точка входа для запуска API сервера
"""

import uvicorn
from src.config import settings
from loguru import logger

if __name__ == "__main__":
    logger.info(f"🚀 Запуск Crypto Analytics API на {settings.host}:{settings.port}")
    
    # Запуск сервера
    uvicorn.run(
        "src.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    ) 