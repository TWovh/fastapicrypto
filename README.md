# FastAPI Crypto Analytics API

API для аналитики криптовалют с расширенными возможностями технического анализа и рыночной аналитики.

## Возможности

- Получение цен топ криптовалют с расширенной аналитикой
- Детальная информация о конкретной криптовалюте
- Поиск криптовалют
- Рыночная аналитика (топ гейнеры/лузеры, распределение капитализации)
- Технический анализ с множественными индикаторами
- История цен криптовалют
- Трендовые криптовалюты

- WebSocket для обновлений в реальном времени
- Асинхронные запросы к внешнему API

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

Или с помощью uvicorn:
```bash
uvicorn main:app --reload
```

Сервер запустится на `http://localhost:8000`

## API Endpoints

### GET /
Корневой эндпоинт с приветствием

### GET /health
Проверка здоровья API

### GET /crypto/prices
Получить цены топ криптовалют
- **Параметры:**
  - `limit` (int, опционально): количество криптовалют (по умолчанию 10)

### GET /crypto/{coin_id}
Получить детальную информацию о криптовалюте
- **Параметры:**
  - `coin_id` (string): ID криптовалюты (например, "bitcoin", "ethereum")

### GET /crypto/search/{query}
Поиск криптовалют
- **Параметры:**
  - `query` (string): поисковый запрос

### GET /crypto/market-data
Получить общую рыночную аналитику
- **Возвращает:** общую капитализацию, объем, топ гейнеров/лузеров, распределение капитализации

### GET /crypto/trending
Получить трендовые криптовалюты
- **Возвращает:** список трендовых монет с их рейтингами

### GET /crypto/{coin_id}/technical-analysis
Получить технический анализ криптовалюты
- **Параметры:**
  - `coin_id` (string): ID криптовалюты
  - `days` (int, опционально): период анализа в днях (по умолчанию 30)
- **Возвращает:** RSI, MACD, Bollinger Bands, SMA, анализ тренда, уровни поддержки/сопротивления

### GET /crypto/{coin_id}/price-history
Получить историю цен криптовалюты
- **Параметры:**
  - `coin_id` (string): ID криптовалюты
  - `days` (int, опционально): период в днях (по умолчанию 30)
  - `currency` (string, опционально): валюта (по умолчанию "usd")



### WebSocket /ws
WebSocket соединение для получения обновлений цен в реальном времени
- **Поддерживаемые действия:**
  - `subscribe`: подписка на обновления конкретной монеты
  - `unsubscribe`: отписка от обновлений
  - `get_prices`: получение текущих цен

## Документация API

После запуска сервера, документация доступна по адресу:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Примеры использования

```bash
# Получить топ 5 криптовалют
curl http://localhost:8000/crypto/prices?limit=5

# Получить информацию о Bitcoin
curl http://localhost:8000/crypto/bitcoin

# Получить технический анализ Bitcoin
curl http://localhost:8000/crypto/bitcoin/technical-analysis?days=30

# Получить историю цен Bitcoin
curl http://localhost:8000/crypto/bitcoin/price-history?days=7

# Получить рыночную аналитику
curl http://localhost:8000/crypto/market-data

# Получить трендовые монеты
curl http://localhost:8000/crypto/trending

# Поиск криптовалют
curl http://localhost:8000/crypto/search/bitcoin


```

## Технологии

- FastAPI
- Pydantic
- httpx (асинхронные HTTP запросы)
- numpy (математические вычисления)
- websockets (WebSocket соединения)
- CoinGecko API 