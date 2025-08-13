# Crypto Analytics API

API для аналитики криптовалют с реальными данными от CoinMarketCap, техническим анализом и WebSocket обновлениями.

> **Последнее обновление**: 13 августа 2025 - Реорганизация проекта и интеграция с CoinMarketCap API

## 🏗️ Структура проекта

```
FastApiCrypto/
├── backend/                 # Backend API
│   ├── src/                # Исходный код
│   │   ├── main.py         # Основное приложение FastAPI
│   │   ├── coinmarketcap_client.py  # Клиент CoinMarketCap API
│   │   ├── websocket_manager.py     # WebSocket менеджер
│   │   ├── technical_analysis.py    # Технический анализ
│   │   └── metrics.py      # Метрики Prometheus
│   ├── main.py             # Точка входа
│   ├── requirements.txt    # Зависимости Python
│   ├── env.example         # Пример переменных окружения
│   ├── Dockerfile          # Docker конфигурация
│   ├── docker-compose.yml  # Docker Compose
│   ├── grafana/            # Конфигурация Grafana
│   ├── prometheus/         # Конфигурация Prometheus
│   └── logs/               # Логи приложения
├── frontend/               # Frontend (будущий)
└── README.md              # Документация
```

## 🚀 Быстрый старт

### 1. Настройка API ключа CoinMarketCap

1. Получите бесплатный API ключ на [CoinMarketCap](https://coinmarketcap.com/api/)
2. Скопируйте `backend/env.example` в `backend/.env`
3. Вставьте ваш API ключ в переменную `COINMARKETCAP_API_KEY`

```bash
# В файле backend/.env
COINMARKETCAP_API_KEY=ваш_реальный_ключ_здесь
```

**🔒 Безопасность**: Файл `.env` не попадает в Git репозиторий, ваш API ключ останется в безопасности!

### 2. Установка зависимостей

```bash
cd backend
pip install -r requirements.txt
```

### 3. Запуск API

```bash
# Из папки backend
python main.py
```

### 4. Запуск с мониторингом (Grafana + Prometheus)

```bash
cd backend
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
- **Вызовы CoinMarketCap API**: `/metrics`

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

### Информация о Bitcoin:
```bash
curl http://localhost:8000/crypto/BTC
```

### Технический анализ Bitcoin:
```bash
curl http://localhost:8000/crypto/BTC/technical-analysis?days=30
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
- **CoinMarketCap API** - источник данных
- **WebSocket** - real-time обновления
- **Prometheus** - сбор метрик
- **Grafana** - визуализация

### Метрики:
- HTTP запросы и время ответа
- Вызовы CoinMarketCap API
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

Все запросы и ошибки логируются в `backend/logs/api.log` и доступны в метриках Prometheus.

## 🚀 Деплой

### Docker:
```bash
cd backend
docker-compose up -d
```

### Локально:
```bash
cd backend
python main.py
```

## 📊 Дашборды Grafana

Автоматически создается дашборд с:
- HTTP запросами по эндпоинтам
- Временем ответа API
- WebSocket соединениями
- Ценами криптовалют
- Ошибками и исключениями
- Вызовами CoinMarketCap API

## 🔑 API Ключ CoinMarketCap

Для работы с API необходимо получить бесплатный ключ:
1. Зарегистрируйтесь на [CoinMarketCap](https://coinmarketcap.com/api/)
2. Выберите бесплатный план
3. Скопируйте API ключ
4. Добавьте в `backend/.env`

**Примечание**: Бесплатный план имеет ограничения:
- 10,000 запросов в месяц
- Базовые эндпоинты
- Исторические данные требуют платную подписку

## 🆕 Что нового в v2.0

- ✅ Интеграция с CoinMarketCap API
- ✅ Реорганизация структуры проекта
- ✅ Улучшенная обработка ошибок
- ✅ Поддержка переменных окружения
- ✅ Структурированное логирование
- ✅ Готовность к frontend разработке 