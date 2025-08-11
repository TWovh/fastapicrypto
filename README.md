# Crypto Analytics API

API для аналитики криптовалют с реальными данными, техническим анализом и WebSocket обновлениями.

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск API
```bash
uvicorn main:app --reload
```

### 3. Запуск с мониторингом (Grafana + Prometheus)
```bash
docker-compose up -d
```

## 📊 Мониторинг

### Доступ к сервисам:
- **API**: http://localhost:8000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Swagger**: http://localhost:8000/docs

### Метрики Prometheus:
- **HTTP запросы**: `/metrics`
- **Время ответа**: `/metrics`
- **WebSocket соединения**: `/metrics`
- **Цены криптовалют**: `/metrics`

## 🔧 API Endpoints

### Основные эндпоинты:
- `GET /` - Информация об API
- `GET /health` - Проверка здоровья
- `GET /metrics` - Метрики Prometheus
- `GET /crypto/prices` - Цены криптовалют
- `GET /crypto/{coin_id}` - Информация о монете
- `GET /crypto/search/{query}` - Поиск криптовалют
- `GET /crypto/market-data` - Рыночные данные
- `GET /crypto/trending` - Трендовые монеты
- `GET /crypto/{coin_id}/technical-analysis` - Технический анализ
- `GET /crypto/{coin_id}/price-history` - История цен
- `WS /ws` - WebSocket для real-time обновлений

## 📈 Примеры использования

### Получение цен криптовалют:
```bash
curl http://localhost:8000/crypto/prices?limit=10
```

### Технический анализ Bitcoin:
```bash
curl http://localhost:8000/crypto/bitcoin/technical-analysis?days=30
```

### WebSocket подключение:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    console.log('Получены данные:', JSON.parse(event.data));
};
```

## 🏗️ Архитектура

### Компоненты:
- **FastAPI** - веб-фреймворк
- **CoinGecko API** - источник данных
- **WebSocket** - real-time обновления
- **Prometheus** - сбор метрик
- **Grafana** - визуализация

### Метрики:
- HTTP запросы и время ответа
- Вызовы внешних API
- WebSocket соединения
- Цены криптовалют
- Ошибки и исключения

## 🔍 Технический анализ

Поддерживаемые индикаторы:
- **SMA/EMA** - скользящие средние
- **RSI** - индекс относительной силы
- **MACD** - схождение/расхождение
- **Bollinger Bands** - полосы Боллинджера
- **Support/Resistance** - уровни поддержки/сопротивления
- **Volume Analysis** - анализ объемов

## 📝 Логирование

Все запросы и ошибки логируются и доступны в метриках Prometheus.

## 🚀 Деплой

### Docker:
```bash
docker-compose up -d
```

### Локально:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📊 Дашборды Grafana

Автоматически создается дашборд с:
- HTTP запросами по эндпоинтам
- Временем ответа API
- WebSocket соединениями
- Ценами криптовалют
- Ошибками и исключениями
- Вызовами CoinGecko API 