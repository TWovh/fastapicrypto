from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time
from functools import wraps

# Метрики для HTTP запросов
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Метрики для API вызовов
API_CALLS = Counter(
    'coinmarketcap_api_calls_total',
    'Total CoinMarketCap API calls',
    ['endpoint', 'status']
)

API_CALL_DURATION = Histogram(
    'coinmarketcap_api_call_duration_seconds',
    'CoinMarketCap API call duration in seconds',
    ['endpoint']
)

# Метрики для WebSocket
WEBSOCKET_CONNECTIONS = Gauge(
    'websocket_connections_current',
    'Current WebSocket connections'
)

WEBSOCKET_MESSAGES = Counter(
    'websocket_messages_total',
    'Total WebSocket messages sent',
    ['coin_symbol']
)

# Метрики для ошибок
ERROR_COUNT = Counter(
    'api_errors_total',
    'Total API errors',
    ['error_type', 'endpoint']
)

# Метрики для криптовалют
CRYPTO_PRICE = Gauge(
    'crypto_price_usd',
    'Current crypto price in USD',
    ['symbol']
)

CRYPTO_MARKET_CAP = Gauge(
    'crypto_market_cap_usd',
    'Current crypto market cap in USD',
    ['symbol']
)

def track_request_metrics(func):
    """Декоратор для отслеживания метрик HTTP запросов"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            status = 200
            REQUEST_COUNT.labels(
                method='GET',
                endpoint=func.__name__,
                status=status
            ).inc()
            return result
        except Exception as e:
            status = 500
            REQUEST_COUNT.labels(
                method='GET',
                endpoint=func.__name__,
                status=status
            ).inc()
            ERROR_COUNT.labels(
                error_type=type(e).__name__,
                endpoint=func.__name__
            ).inc()
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(
                method='GET',
                endpoint=func.__name__
            ).observe(duration)
    
    return wrapper

def track_api_call(endpoint: str):
    """Декоратор для отслеживания вызовов внешних API"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                API_CALLS.labels(endpoint=endpoint, status='success').inc()
                return result
            except Exception as e:
                API_CALLS.labels(endpoint=endpoint, status='error').inc()
                raise
            finally:
                duration = time.time() - start_time
                API_CALL_DURATION.labels(endpoint=endpoint).observe(duration)
        
        return wrapper
    return decorator

def get_metrics():
    """Эндпоинт для получения метрик Prometheus"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

def update_crypto_metrics(symbol: str, price: float, market_cap: float = None):
    """Обновление метрик криптовалют"""
    CRYPTO_PRICE.labels(symbol=symbol.upper()).set(price)
    if market_cap:
        CRYPTO_MARKET_CAP.labels(symbol=symbol.upper()).set(market_cap)

def increment_websocket_connection():
    """Увеличение счетчика WebSocket соединений"""
    WEBSOCKET_CONNECTIONS.inc()

def decrement_websocket_connection():
    """Уменьшение счетчика WebSocket соединений"""
    WEBSOCKET_CONNECTIONS.dec()

def increment_websocket_message(coin_symbol: str):
    """Увеличение счетчика WebSocket сообщений"""
    WEBSOCKET_MESSAGES.labels(coin_symbol=coin_symbol.upper()).inc()

def setup_metrics(app):
    """Настройка метрик для FastAPI приложения"""
    @app.get("/metrics")
    async def metrics_endpoint():
        return get_metrics()

def record_request(endpoint: str):
    """Запись метрики HTTP запроса"""
    REQUEST_COUNT.labels(
        method='GET',
        endpoint=endpoint,
        status=200
    ).inc()

def record_api_call(api_name: str, endpoint: str):
    """Запись метрики вызова API"""
    API_CALLS.labels(
        endpoint=f"{api_name}_{endpoint}",
        status='success'
    ).inc() 