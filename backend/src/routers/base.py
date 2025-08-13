from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..config import settings
from ..metrics import get_metrics
from loguru import logger

router = APIRouter(
    tags=["base"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root() -> Dict[str, Any]:
    """
    Корневой эндпоинт API
    """
    return {
        "message": "🚀 Crypto Analytics API",
        "version": settings.api_version,
        "description": settings.api_description,
        "endpoints": {
            "crypto": "/crypto",
            "technical": "/technical", 
            "websocket": "/ws",
            "docs": "/docs",
            "health": "/health",
            "metrics": "/metrics"
        }
    }

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Проверка здоровья API
    """
    return {
        "status": "healthy",
        "version": settings.api_version,
        "api_key_configured": bool(settings.coinmarketcap_api_key and settings.coinmarketcap_api_key != "your_api_key_here")
    }

@router.get("/metrics")
async def metrics() -> Dict[str, Any]:
    """
    Метрики Prometheus
    """
    try:
        return get_metrics()
    except Exception as e:
        logger.error(f"Ошибка получения метрик: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения метрик")

@router.get("/info")
async def api_info() -> Dict[str, Any]:
    """
    Информация об API
    """
    return {
        "title": settings.api_title,
        "description": settings.api_description,
        "version": settings.api_version,
        "host": settings.host,
        "port": settings.port,
        "debug": settings.debug
    } 