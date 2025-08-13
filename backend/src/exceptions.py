from fastapi import HTTPException
from typing import Any, Dict, Optional

class CryptoAPIException(Exception):
    """Базовое исключение для API"""
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class CoinNotFoundError(CryptoAPIException):
    """Монета не найдена"""
    def __init__(self, coin_id: str):
        super().__init__(
            message=f"Монета '{coin_id}' не найдена",
            status_code=404,
            details={"coin_id": coin_id}
        )

class APIKeyMissingError(CryptoAPIException):
    """API ключ отсутствует"""
    def __init__(self):
        super().__init__(
            message="API ключ CoinMarketCap не настроен",
            status_code=500,
            details={"error_type": "configuration_error"}
        )

class InsufficientDataError(CryptoAPIException):
    """Недостаточно данных для анализа"""
    def __init__(self, required: int, available: int):
        super().__init__(
            message=f"Недостаточно данных для анализа. Требуется: {required}, доступно: {available}",
            status_code=400,
            details={"required": required, "available": available}
        )

class ExternalAPIError(CryptoAPIException):
    """Ошибка внешнего API"""
    def __init__(self, api_name: str, status_code: int, message: str):
        super().__init__(
            message=f"Ошибка {api_name} API: {message}",
            status_code=status_code,
            details={"api_name": api_name, "external_status_code": status_code}
        )

class ValidationError(CryptoAPIException):
    """Ошибка валидации данных"""
    def __init__(self, field: str, value: Any, constraint: str):
        super().__init__(
            message=f"Ошибка валидации поля '{field}': значение {value} не соответствует ограничению {constraint}",
            status_code=400,
            details={"field": field, "value": value, "constraint": constraint}
        )

def raise_http_exception(exception: CryptoAPIException) -> HTTPException:
    """Преобразует кастомное исключение в HTTPException"""
    return HTTPException(
        status_code=exception.status_code,
        detail={
            "error": exception.message,
            "details": exception.details
        }
    ) 