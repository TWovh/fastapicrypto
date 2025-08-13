import time
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования HTTP запросов и ответов
    
    Как работает:
    1. Перехватывает каждый HTTP запрос
    2. Логирует информацию о запросе (метод, URL, время)
    3. Пропускает запрос к обработчику
    4. Логирует информацию об ответе (статус, время выполнения)
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Время начала обработки запроса
        start_time = time.time()
        
        # Логируем входящий запрос
        logger.info(
            f"📥 Входящий запрос: {request.method} {request.url.path} "
            f"| IP: {request.client.host if request.client else 'unknown'} "
            f"| User-Agent: {request.headers.get('user-agent', 'unknown')}"
        )
        
        # Если есть query параметры, логируем их
        if request.query_params:
            logger.debug(f"🔍 Query параметры: {dict(request.query_params)}")
        
        # Если есть тело запроса, логируем его (только для POST/PUT)
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    logger.debug(f"📦 Тело запроса: {body.decode()[:200]}...")
            except Exception as e:
                logger.warning(f"⚠️ Не удалось прочитать тело запроса: {e}")
        
        # Пропускаем запрос к следующему обработчику
        try:
            response = await call_next(request)
            
            # Вычисляем время выполнения
            process_time = time.time() - start_time
            
            # Логируем исходящий ответ
            logger.info(
                f"📤 Исходящий ответ: {request.method} {request.url.path} "
                f"| Статус: {response.status_code} "
                f"| Время: {process_time:.3f}s "
                f"| Размер: {len(response.body) if hasattr(response, 'body') else 'unknown'} bytes"
            )
            
            # Добавляем время выполнения в заголовки ответа
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Логируем ошибки
            process_time = time.time() - start_time
            logger.error(
                f"❌ Ошибка обработки: {request.method} {request.url.path} "
                f"| Ошибка: {str(e)} "
                f"| Время: {process_time:.3f}s"
            )
            raise

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для детального логирования ошибок
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            # Логируем детальную информацию об ошибке
            logger.error(
                f"🚨 Критическая ошибка: {request.method} {request.url.path}",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "request_url": str(request.url),
                    "request_method": request.method,
                    "client_ip": request.client.host if request.client else "unknown",
                    "user_agent": request.headers.get("user-agent", "unknown")
                }
            )
            raise

class PerformanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware для мониторинга производительности
    """
    
    def __init__(self, app, slow_request_threshold: float = 1.0):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Логируем медленные запросы
        if process_time > self.slow_request_threshold:
            logger.warning(
                f"🐌 Медленный запрос: {request.method} {request.url.path} "
                f"| Время: {process_time:.3f}s "
                f"| Порог: {self.slow_request_threshold}s"
            )
        
        return response 