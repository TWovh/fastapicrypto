import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Импорт конфигурации и middleware
from .config import settings
from .middleware.logging import LoggingMiddleware, ErrorLoggingMiddleware, PerformanceMiddleware

# Импорт роутеров
from .routers import base, crypto, technical, websocket

# Импорт обработчиков ошибок
from .exceptions import CryptoAPIException, raise_http_exception

# Настройка логирования
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
logger.add(settings.log_file, rotation="1 day", retention="7 days", level=settings.log_level)

# Инициализация FastAPI приложения
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Добавление middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorLoggingMiddleware)
app.add_middleware(PerformanceMiddleware, slow_request_threshold=1.0)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(base.router)
app.include_router(crypto.router)
app.include_router(technical.router)
app.include_router(websocket.router)

# Глобальный обработчик исключений
@app.exception_handler(CryptoAPIException)
async def crypto_api_exception_handler(request, exc: CryptoAPIException):
    """Обработчик кастомных исключений"""
    logger.error(f"API ошибка: {exc.message}", extra=exc.details)
    return raise_http_exception(exc)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Глобальный обработчик исключений"""
    logger.error(f"Неожиданная ошибка: {str(exc)}")
    return HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    logger.info("🚀 Запуск Crypto Analytics API")
    logger.info(f"📊 Версия: {settings.api_version}")
    logger.info(f"🌐 Хост: {settings.host}:{settings.port}")
    logger.info(f"🔧 Режим отладки: {settings.debug}")
    
    # Проверка API ключа
    if not settings.coinmarketcap_api_key or settings.coinmarketcap_api_key == "your_api_key_here":
        logger.warning("⚠️ API ключ CoinMarketCap не настроен!")
        logger.info("📝 Для настройки API ключа:")
        logger.info("   1. Получите ключ на https://coinmarketcap.com/api/")
        logger.info("   2. Скопируйте backend/env.example в backend/.env")
        logger.info("   3. Вставьте ваш ключ в COINMARKETCAP_API_KEY")

@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при завершении"""
    logger.info("🛑 Остановка Crypto Analytics API") 