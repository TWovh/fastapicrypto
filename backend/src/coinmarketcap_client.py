import httpx
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from loguru import logger
from .config import settings

class CoinMarketCapClient:
    """Клиент для работы с CoinMarketCap API"""
    
    def __init__(self):
        self.api_key = settings.coinmarketcap_api_key
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        self.headers = {
            'X-CMC_PRO_API_KEY': self.api_key,
            'Accept': 'application/json'
        }
        
        if not self.api_key or self.api_key == "your_api_key_here":
            logger.warning("⚠️ API ключ CoinMarketCap не настроен!")
            logger.info("📝 Для настройки API ключа:")
            logger.info("   1. Получите ключ на https://coinmarketcap.com/api/")
            logger.info("   2. Скопируйте backend/env.example в backend/.env")
            logger.info("   3. Вставьте ваш ключ в COINMARKETCAP_API_KEY")
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполнение HTTP запроса к API"""
        if not self.api_key or self.api_key == "your_api_key_here":
            raise Exception("API ключ CoinMarketCap не настроен")
        
        url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP ошибка {e.response.status_code}: {e.response.text}")
                raise Exception(f"API ошибка: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Ошибка запроса к CoinMarketCap API: {e}")
                raise
    
    async def get_status(self) -> bool:
        """Проверка статуса API"""
        try:
            # Простой запрос для проверки API
            await self._make_request("cryptocurrency/listings/latest", {"limit": 1})
            return True
        except Exception:
            return False
    
    async def get_crypto_prices(self, limit: int = 100, convert: str = "USD") -> List[Dict[str, Any]]:
        """Получение цен криптовалют"""
        params = {
            "limit": limit,
            "convert": convert,
            "sort": "market_cap",
            "sort_dir": "desc"
        }
        
        data = await self._make_request("cryptocurrency/listings/latest", params)
        
        prices = []
        for coin in data.get("data", []):
            quote = coin.get("quote", {}).get(convert, {})
            prices.append({
                "id": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "price": quote.get("price", 0),
                "market_cap": quote.get("market_cap", 0),
                "volume_24h": quote.get("volume_24h", 0),
                "change_24h": quote.get("percent_change_24h", 0),
                "last_updated": coin.get("last_updated")
            })
        
        return prices
    
    async def get_coin_info(self, coin_id: str) -> Dict[str, Any]:
        """Получение информации о конкретной монете"""
        params = {
            "symbol": coin_id.upper(),
            "convert": "USD"
        }
        
        data = await self._make_request("cryptocurrency/quotes/latest", params)
        
        if not data.get("data"):
            raise Exception("Монета не найдена")
        
        coin_data = list(data["data"].values())[0]
        quote = coin_data.get("quote", {}).get("USD", {})
        
        return {
            "id": coin_data.get("id"),
            "name": coin_data.get("name"),
            "symbol": coin_data.get("symbol"),
            "slug": coin_data.get("slug"),
            "price": quote.get("price", 0),
            "market_cap": quote.get("market_cap", 0),
            "volume_24h": quote.get("volume_24h", 0),
            "change_1h": quote.get("percent_change_1h", 0),
            "change_24h": quote.get("percent_change_24h", 0),
            "change_7d": quote.get("percent_change_7d", 0),
            "circulating_supply": coin_data.get("circulating_supply"),
            "total_supply": coin_data.get("total_supply"),
            "max_supply": coin_data.get("max_supply"),
            "cmc_rank": coin_data.get("cmc_rank"),
            "last_updated": coin_data.get("last_updated"),
            "tags": coin_data.get("tags", []),
            "platform": coin_data.get("platform"),
            "description": coin_data.get("description")
        }
    
    async def search_cryptocurrencies(self, query: str) -> List[Dict[str, Any]]:
        """Поиск криптовалют"""
        params = {
            "query": query,
            "limit": 10
        }
        
        data = await self._make_request("cryptocurrency/map", params)
        
        results = []
        for coin in data.get("data", []):
            results.append({
                "id": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "slug": coin.get("slug"),
                "rank": coin.get("rank"),
                "is_active": coin.get("is_active"),
                "first_historical_data": coin.get("first_historical_data"),
                "last_historical_data": coin.get("last_historical_data")
            })
        
        return results
    
    async def get_market_data(self) -> Dict[str, Any]:
        """Получение общих рыночных данных"""
        params = {
            "convert": "USD"
        }
        
        data = await self._make_request("global-metrics/quotes/latest", params)
        global_data = data.get("data", {})
        quote = global_data.get("quote", {}).get("USD", {})
        
        return {
            "total_market_cap": quote.get("total_market_cap", 0),
            "total_volume_24h": quote.get("total_volume_24h", 0),
            "market_cap_percentage": quote.get("market_cap_dominance", {}),
            "market_cap_change_24h": quote.get("total_market_cap_yesterday_percentage_change", 0),
            "active_cryptocurrencies": global_data.get("active_cryptocurrencies", 0),
            "total_cryptocurrencies": global_data.get("total_cryptocurrencies", 0),
            "active_market_pairs": global_data.get("active_market_pairs", 0),
            "last_updated": global_data.get("last_updated")
        }
    
    async def get_trending_coins(self) -> List[Dict[str, Any]]:
        """Получение трендовых монет (топ по изменению цены)"""
        params = {
            "limit": 20,
            "convert": "USD",
            "sort": "percent_change_24h",
            "sort_dir": "desc"
        }
        
        data = await self._make_request("cryptocurrency/listings/latest", params)
        
        trending = []
        for coin in data.get("data", [])[:10]:  # Топ 10
            quote = coin.get("quote", {}).get("USD", {})
            trending.append({
                "id": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "price": quote.get("price", 0),
                "change_24h": quote.get("percent_change_24h", 0),
                "volume_24h": quote.get("volume_24h", 0),
                "market_cap": quote.get("market_cap", 0)
            })
        
        return trending
    
    async def get_historical_data(self, coin_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Получение исторических данных"""
        # CoinMarketCap Pro API требует платную подписку для исторических данных
        # Для демонстрации используем текущие данные
        logger.warning("Исторические данные требуют платную подписку CoinMarketCap Pro")
        
        try:
            coin_info = await self.get_coin_info(coin_id)
            
            # Создаем демо-данные на основе текущей цены
            current_price = coin_info["price"]
            historical_data = []
            
            for i in range(days):
                date = datetime.now() - timedelta(days=days - i - 1)
                # Имитируем изменение цены
                price_change = (i % 7 - 3) * 0.02  # ±6% изменение
                price = current_price * (1 + price_change)
                
                historical_data.append({
                    "timestamp": date.isoformat(),
                    "price": price,
                    "volume": coin_info["volume_24h"] * (0.8 + 0.4 * (i % 5) / 5),
                    "market_cap": coin_info["market_cap"] * (1 + price_change)
                })
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Ошибка получения исторических данных: {e}")
            raise Exception("Не удалось получить исторические данные")
    
    async def get_exchange_rates(self, convert: str = "USD") -> Dict[str, float]:
        """Получение курсов валют"""
        params = {
            "convert": convert
        }
        
        data = await self._make_request("tools/price-conversion", params)
        
        rates = {}
        for quote in data.get("data", []):
            symbol = quote.get("symbol")
            price = quote.get("quote", {}).get(convert, {}).get("price", 0)
            rates[symbol] = price
        
        return rates 