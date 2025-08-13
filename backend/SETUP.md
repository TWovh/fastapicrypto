# Настройка CoinMarketCap API

## 🔑 Получение API ключа

### 1. Регистрация
1. Перейдите на [CoinMarketCap API](https://coinmarketcap.com/api/)
2. Нажмите "Get Started"
3. Зарегистрируйтесь или войдите в аккаунт

### 2. Выбор плана
- **Basic (Бесплатный)**: 10,000 запросов в месяц
- **Hobbyist**: 50,000 запросов в месяц ($23/месяц)
- **Startup**: 500,000 запросов в месяц ($79/месяц)
- **Standard**: 5,000,000 запросов в месяц ($279/месяц)

### 3. Получение ключа
1. Выберите бесплатный план "Basic"
2. Скопируйте ваш API ключ

## ⚙️ Настройка проекта

### 1. Создание файла .env
```bash
# В папке backend
cp env.example .env
```

### 2. Добавление API ключа
Откройте файл `backend/.env` и замените:
```env
COINMARKETCAP_API_KEY=your_api_key_here
```
на:
```env
COINMARKETCAP_API_KEY=ваш_реальный_ключ_здесь
```

**⚠️ ВАЖНО**: Файл `.env` НЕ попадает в Git репозиторий (добавлен в .gitignore), поэтому ваш API ключ останется в безопасности!

### 3. Проверка настройки
```bash
cd backend
python main.py
```

В логах должно появиться:
```
🚀 Запуск Crypto Analytics API
📊 Используется CoinMarketCap API
```

## 📊 Доступные эндпоинты (Basic план)

### ✅ Доступно бесплатно:
- `/crypto/prices` - Цены криптовалют
- `/crypto/{coin_id}` - Информация о монете
- `/crypto/search/{query}` - Поиск криптовалют
- `/crypto/market-data` - Рыночные данные
- `/crypto/trending` - Трендовые монеты

### ❌ Требует платную подписку:
- `/crypto/{coin_id}/technical-analysis` - Исторические данные
- `/crypto/{coin_id}/price-history` - История цен

## 🔧 Тестирование API

### Проверка подключения:
```bash
curl http://localhost:8000/health
```

### Получение цен:
```bash
curl http://localhost:8000/crypto/prices?limit=5
```

### Информация о Bitcoin:
```bash
curl http://localhost:8000/crypto/BTC
```

## ⚠️ Ограничения бесплатного плана

- **10,000 запросов в месяц**
- **Обновление данных**: каждые 5 минут
- **Исторические данные**: недоступны
- **WebSocket**: недоступен

## 🚀 Обновление до платного плана

Если нужны дополнительные возможности:
1. Перейдите в [CoinMarketCap API Dashboard](https://pro.coinmarketcap.com/)
2. Выберите подходящий план
3. Обновите API ключ в `.env`
4. Перезапустите приложение

## 📝 Логирование

Все запросы к API логируются в:
- `backend/logs/api.log`
- Метрики Prometheus: `http://localhost:8000/metrics`

## 🔍 Отладка

### Проверка API ключа:
```python
import os
from decouple import config

api_key = config('COINMARKETCAP_API_KEY')
print(f"API Key: {api_key[:10]}..." if api_key else "API Key not found")
```

### Тест подключения:
```bash
curl -H "X-CMC_PRO_API_KEY: YOUR_API_KEY" \
     "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=1"
```

## 🔒 Безопасность

- ✅ Файл `.env` добавлен в `.gitignore`
- ✅ API ключ НЕ попадает в репозиторий
- ✅ Переменные окружения загружаются безопасно
- ✅ Логи не содержат API ключ

## 🚨 Если API ключ не работает

1. Проверьте правильность ключа
2. Убедитесь, что файл `.env` создан в папке `backend/`
3. Проверьте лимиты бесплатного плана
4. Перезапустите приложение после изменения `.env` 