from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv
from websocket_handler import websocket_handler
from technical_analysis import TechnicalAnalysis
import datetime

load_dotenv()

app = FastAPI(
    title="Crypto Analytics API",
    description="API для аналитики криптовалют с реальными данными",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class CryptoPrice(BaseModel):
    symbol: str
    price: float
    change_24h: Optional[float] = None
    change_percentage_24h: Optional[float] = None
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None

class CryptoInfo(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: float
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None

class MarketData(BaseModel):
    total_market_cap: float
    total_volume: float
    market_cap_percentage: Dict[str, float]
    top_gainers: List[CryptoPrice]
    top_losers: List[CryptoPrice]



# Конфигурация
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Добро пожаловать в Crypto Analytics API!", 
        "version": "1.0.0",
        "endpoints": {
            "prices": "/crypto/prices",
            "info": "/crypto/{coin_id}",
            "search": "/crypto/search/{query}",
            "market_data": "/crypto/market-data",
            "trending": "/crypto/trending",
            "technical_analysis": "/crypto/{coin_id}/technical-analysis",
            "price_history": "/crypto/{coin_id}/price-history",
            "websocket": "/ws"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy", "service": "crypto-analytics-api"}

@app.get("/crypto/prices", response_model=List[CryptoPrice])
async def get_crypto_prices(limit: int = 20, currency: str = "usd"):
    """Получить цены топ криптовалют с расширенной аналитикой"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{COINGECKO_API_BASE}/coins/markets",
                params={
                    "vs_currency": currency,
                    "order": "market_cap_desc",
                    "per_page": limit,
                    "page": 1,
                    "sparkline": False
                }
            )
            response.raise_for_status()
            data = response.json()
            
            crypto_prices = []
            for coin in data:
                crypto_prices.append(CryptoPrice(
                    symbol=coin["symbol"].upper(),
                    price=coin["current_price"],
                    change_24h=coin.get("price_change_24h"),
                    change_percentage_24h=coin.get("price_change_percentage_24h"),
                    market_cap=coin.get("market_cap"),
                    volume_24h=coin.get("total_volume"),
                    high_24h=coin.get("high_24h"),
                    low_24h=coin.get("low_24h")
                ))
            
            return crypto_prices
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Превышен лимит запросов к API. Попробуйте позже.")
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@app.get("/crypto/{coin_id}", response_model=CryptoInfo)
async def get_crypto_info(coin_id: str):
    """Получить детальную информацию о криптовалюте"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{COINGECKO_API_BASE}/coins/{coin_id}")
            response.raise_for_status()
            data = response.json()
            
            market_data = data.get("market_data", {})
            return CryptoInfo(
                id=data["id"],
                symbol=data["symbol"].upper(),
                name=data["name"],
                current_price=market_data.get("current_price", {}).get("usd", 0),
                market_cap=market_data.get("market_cap", {}).get("usd"),
                volume_24h=market_data.get("total_volume", {}).get("usd"),
                price_change_24h=market_data.get("price_change_24h"),
                price_change_percentage_24h=market_data.get("price_change_percentage_24h"),
                high_24h=market_data.get("high_24h", {}).get("usd"),
                low_24h=market_data.get("low_24h", {}).get("usd"),
                circulating_supply=market_data.get("circulating_supply"),
                total_supply=market_data.get("total_supply"),
                max_supply=market_data.get("max_supply")
            )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Превышен лимит запросов к API. Попробуйте позже.")
        else:
            raise HTTPException(status_code=404, detail=f"Криптовалюта не найдена: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Криптовалюта не найдена: {str(e)}")

@app.get("/crypto/search/{query}")
async def search_crypto(query: str):
    """Поиск криптовалют"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{COINGECKO_API_BASE}/search", params={"query": query})
            response.raise_for_status()
            data = response.json()
            
            return {
                "query": query,
                "results": data["coins"][:10]  # Возвращаем топ 10 результатов
            }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Превышен лимит запросов к API. Попробуйте позже.")
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка при поиске: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске: {str(e)}")

@app.get("/crypto/market-data", response_model=MarketData)
async def get_market_data():
    """Получить общую рыночную аналитику"""
    try:
        async with httpx.AsyncClient() as client:
            # Получаем топ 100 криптовалют для анализа
            response = await client.get(
                f"{COINGECKO_API_BASE}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 100,
                    "page": 1,
                    "sparkline": False
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Вычисляем общую рыночную капитализацию и объем
            total_market_cap = sum(coin.get("market_cap", 0) for coin in data)
            total_volume = sum(coin.get("total_volume", 0) for coin in data)
            
            # Вычисляем процентное распределение по капитализации
            market_cap_percentage = {}
            for coin in data[:10]:  # Топ 10
                if coin.get("market_cap") and total_market_cap > 0:
                    market_cap_percentage[coin["symbol"].upper()] = (coin["market_cap"] / total_market_cap) * 100
            
            # Находим топ гейнеров и лузеров
            sorted_by_change = sorted(data, key=lambda x: x.get("price_change_percentage_24h", 0), reverse=True)
            top_gainers = []
            top_losers = []
            
            for coin in sorted_by_change[:5]:  # Топ 5 гейнеров
                top_gainers.append(CryptoPrice(
                    symbol=coin["symbol"].upper(),
                    price=coin["current_price"],
                    change_24h=coin.get("price_change_24h"),
                    change_percentage_24h=coin.get("price_change_percentage_24h"),
                    market_cap=coin.get("market_cap"),
                    volume_24h=coin.get("total_volume"),
                    high_24h=coin.get("high_24h"),
                    low_24h=coin.get("low_24h")
                ))
            
            for coin in sorted_by_change[-5:]:  # Топ 5 лузеров
                top_losers.append(CryptoPrice(
                    symbol=coin["symbol"].upper(),
                    price=coin["current_price"],
                    change_24h=coin.get("price_change_24h"),
                    change_percentage_24h=coin.get("price_change_percentage_24h"),
                    market_cap=coin.get("market_cap"),
                    volume_24h=coin.get("total_volume"),
                    high_24h=coin.get("high_24h"),
                    low_24h=coin.get("low_24h")
                ))
            
            return MarketData(
                total_market_cap=total_market_cap,
                total_volume=total_volume,
                market_cap_percentage=market_cap_percentage,
                top_gainers=top_gainers,
                top_losers=top_losers
            )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Превышен лимит запросов к API. Попробуйте позже.")
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка при получении рыночных данных: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении рыночных данных: {str(e)}")

@app.get("/crypto/trending")
async def get_trending_coins():
    """Получить трендовые криптовалюты"""
    try:
        async with httpx.AsyncClient() as client:
            # Используем правильный эндпоинт для трендовых монет
            response = await client.get(f"{COINGECKO_API_BASE}/search/trending")
            response.raise_for_status()
            data = response.json()
            
            trending_coins = []
            for coin in data.get("coins", []):
                item = coin.get("item", {})
                trending_coins.append({
                    "id": item.get("id"),
                    "symbol": item.get("symbol", "").upper(),
                    "name": item.get("name"),
                    "market_cap_rank": item.get("market_cap_rank"),
                    "price_btc": item.get("price_btc"),
                    "score": item.get("score")
                })
            
            return {
                "trending_coins": trending_coins,
                "total": len(trending_coins)
            }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            # Если эндпоинт не найден, возвращаем топ монет по изменению цены
            return await get_trending_alternative()
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка при получении трендовых монет: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении трендовых монет: {str(e)}")

async def get_trending_alternative():
    """Альтернативный метод получения трендовых монет"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{COINGECKO_API_BASE}/coins/markets", params={
                "vs_currency": "usd",
                "order": "price_change_percentage_24h_desc",
                "per_page": 10,
                "page": 1,
                "sparkline": False
            })
            response.raise_for_status()
            data = response.json()
            
            trending_coins = []
            for coin in data:
                trending_coins.append({
                    "id": coin["id"],
                    "symbol": coin["symbol"].upper(),
                    "name": coin["name"],
                    "current_price": coin["current_price"],
                    "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
                    "market_cap": coin.get("market_cap"),
                    "volume_24h": coin.get("total_volume")
                })
            
            return {
                "trending_coins": trending_coins,
                "total": len(trending_coins),
                "note": "Показаны топ-10 монет по изменению цены за 24 часа"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении альтернативных трендовых монет: {str(e)}")



@app.get("/crypto/{coin_id}/technical-analysis")
async def get_technical_analysis(coin_id: str, days: int = 30):
    """Получить технический анализ криптовалюты"""
    try:
        async with httpx.AsyncClient() as client:
            # Получаем исторические данные
            response = await client.get(
                f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart",
                params={
                    "vs_currency": "usd",
                    "days": days
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Извлекаем данные о ценах
            prices = [point[1] for point in data["prices"]]
            volumes = [point[1] for point in data["total_volumes"]]
            market_caps = [point[1] for point in data["market_caps"]]
            
            # Вычисляем технические индикаторы
            sma_20 = TechnicalAnalysis.calculate_sma(prices, 20)
            sma_50 = TechnicalAnalysis.calculate_sma(prices, 50)
            rsi = TechnicalAnalysis.calculate_rsi(prices, 14)
            bollinger_bands = TechnicalAnalysis.calculate_bollinger_bands(prices, 20, 2)
            macd = TechnicalAnalysis.calculate_macd(prices, 12, 26, 9)
            
            # Анализ тренда
            trend_analysis = TechnicalAnalysis.get_trend_analysis(prices, 20, 50)
            
            # Анализ объема
            volume_analysis = TechnicalAnalysis.get_volume_analysis(prices, volumes)
            
            # Уровни поддержки и сопротивления
            support_resistance = TechnicalAnalysis.get_support_resistance(prices, 10)
            
            return {
                "coin_id": coin_id,
                "period_days": days,
                "current_price": prices[-1] if prices else 0,
                "price_change_24h": ((prices[-1] - prices[-2]) / prices[-2] * 100) if len(prices) >= 2 else 0,
                "technical_indicators": {
                    "sma_20": sma_20[-1] if sma_20 else None,
                    "sma_50": sma_50[-1] if sma_50 else None,
                    "rsi": rsi[-1] if rsi else None,
                    "bollinger_bands": {
                        "upper": bollinger_bands["upper"][-1] if bollinger_bands["upper"] else None,
                        "middle": bollinger_bands["middle"][-1] if bollinger_bands["middle"] else None,
                        "lower": bollinger_bands["lower"][-1] if bollinger_bands["lower"] else None
                    },
                    "macd": {
                        "macd_line": macd["macd"][-1] if macd["macd"] else None,
                        "signal_line": macd["signal"][-1] if macd["signal"] else None,
                        "histogram": macd["histogram"][-1] if macd["histogram"] else None
                    }
                },
                "trend_analysis": trend_analysis,
                "volume_analysis": volume_analysis,
                "support_resistance": {
                    "support_levels": support_resistance["support"][-3:] if support_resistance["support"] else [],
                    "resistance_levels": support_resistance["resistance"][-3:] if support_resistance["resistance"] else []
                },
                "signals": {
                    "rsi_signal": "перекуплен" if rsi and rsi[-1] > 70 else "перепродан" if rsi and rsi[-1] < 30 else "нейтральный",
                    "macd_signal": "бычий" if macd["histogram"] and macd["histogram"][-1] > 0 else "медвежий",
                    "bollinger_signal": "высокий" if prices and bollinger_bands["upper"] and prices[-1] > bollinger_bands["upper"][-1] else "низкий" if prices and bollinger_bands["lower"] and prices[-1] < bollinger_bands["lower"][-1] else "нейтральный"
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении технического анализа: {str(e)}")

@app.get("/crypto/{coin_id}/price-history")
async def get_price_history(coin_id: str, days: int = 30, currency: str = "usd"):
    """Получить историю цен криптовалюты"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart",
                params={
                    "vs_currency": currency,
                    "days": days
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Форматируем данные
            price_history = []
            for i, (timestamp, price) in enumerate(data["prices"]):
                price_history.append({
                    "timestamp": timestamp,
                    "date": timestamp,  # Можно конвертировать в читаемую дату
                    "price": price,
                    "volume": data["total_volumes"][i][1] if i < len(data["total_volumes"]) else 0,
                    "market_cap": data["market_caps"][i][1] if i < len(data["market_caps"]) else 0
                })
            
            return {
                "coin_id": coin_id,
                "currency": currency,
                "period_days": days,
                "data_points": len(price_history),
                "price_history": price_history
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении истории цен: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket эндпоинт для получения обновлений в реальном времени"""
    await websocket_handler.handle_websocket(websocket)

@app.on_event("startup")
async def startup_event():
    """Запуск мониторинга цен при старте приложения"""
    asyncio.create_task(websocket_handler.start_price_monitoring())

@app.on_event("shutdown")
async def shutdown_event():
    """Остановка мониторинга цен при выключении приложения"""
    websocket_handler.stop_price_monitoring()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 