from typing import List, Dict, Any, Optional
from ..coinmarketcap_client import CoinMarketCapClient
from ..models.crypto import CryptoPrice, CoinInfo, SearchResult, TrendingCoin
from ..exceptions import CoinNotFoundError, ExternalAPIError
from ..constants import Currency, DEFAULT_LIMIT
from loguru import logger

class CryptoService:
    """
    Сервисный слой для работы с криптовалютами
    
    Что это такое:
    - Бизнес-логика отделена от HTTP слоя
    - Обработка данных и трансформация
    - Валидация и обработка ошибок
    - Переиспользование логики
    """
    
    def __init__(self, client: CoinMarketCapClient):
        self.client = client
    
    async def get_crypto_prices(
        self, 
        limit: int = DEFAULT_LIMIT, 
        convert: Currency = Currency.USD
    ) -> List[CryptoPrice]:
        """
        Получение цен криптовалют с обработкой данных
        """
        try:
            # Получаем сырые данные от API
            raw_data = await self.client.get_crypto_prices(limit, convert.value)
            
            # Трансформируем в Pydantic модели
            prices = []
            for item in raw_data:
                try:
                    price = CryptoPrice(
                        id=item["id"],
                        name=item["name"],
                        symbol=item["symbol"],
                        price=item["price"],
                        market_cap=item["market_cap"],
                        volume_24h=item["volume_24h"],
                        change_24h=item["change_24h"],
                        last_updated=item["last_updated"]
                    )
                    prices.append(price)
                except KeyError as e:
                    logger.warning(f"Пропущен элемент с отсутствующим полем: {e}")
                    continue
            
            logger.info(f"Получено {len(prices)} цен криптовалют")
            return prices
            
        except Exception as e:
            logger.error(f"Ошибка получения цен криптовалют: {e}")
            raise ExternalAPIError("CoinMarketCap", 500, str(e))
    
    async def get_coin_info(self, coin_id: str) -> CoinInfo:
        """
        Получение информации о конкретной монете
        """
        try:
            raw_data = await self.client.get_coin_info(coin_id)
            
            # Трансформируем в Pydantic модель
            coin_info = CoinInfo(
                id=raw_data["id"],
                name=raw_data["name"],
                symbol=raw_data["symbol"],
                slug=raw_data["slug"],
                price=raw_data["price"],
                market_cap=raw_data["market_cap"],
                volume_24h=raw_data["volume_24h"],
                change_1h=raw_data["change_1h"],
                change_24h=raw_data["change_24h"],
                change_7d=raw_data["change_7d"],
                circulating_supply=raw_data.get("circulating_supply"),
                total_supply=raw_data.get("total_supply"),
                max_supply=raw_data.get("max_supply"),
                cmc_rank=raw_data.get("cmc_rank"),
                last_updated=raw_data["last_updated"],
                tags=raw_data.get("tags", []),
                platform=raw_data.get("platform"),
                description=raw_data.get("description")
            )
            
            logger.info(f"Получена информация о монете {coin_id}")
            return coin_info
            
        except Exception as e:
            logger.error(f"Ошибка получения информации о монете {coin_id}: {e}")
            raise CoinNotFoundError(coin_id)
    
    async def search_cryptocurrencies(self, query: str) -> List[SearchResult]:
        """
        Поиск криптовалют
        """
        try:
            raw_data = await self.client.search_cryptocurrencies(query)
            
            results = []
            for item in raw_data:
                try:
                    result = SearchResult(
                        id=item["id"],
                        name=item["name"],
                        symbol=item["symbol"],
                        slug=item["slug"],
                        rank=item.get("rank"),
                        is_active=item["is_active"],
                        first_historical_data=item.get("first_historical_data"),
                        last_historical_data=item.get("last_historical_data")
                    )
                    results.append(result)
                except KeyError as e:
                    logger.warning(f"Пропущен результат поиска с отсутствующим полем: {e}")
                    continue
            
            logger.info(f"Найдено {len(results)} результатов для запроса '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"Ошибка поиска криптовалют '{query}': {e}")
            raise ExternalAPIError("CoinMarketCap", 500, str(e))
    
    async def get_trending_coins(self) -> List[TrendingCoin]:
        """
        Получение трендовых монет
        """
        try:
            raw_data = await self.client.get_trending_coins()
            
            trending = []
            for item in raw_data:
                try:
                    coin = TrendingCoin(
                        id=item["id"],
                        name=item["name"],
                        symbol=item["symbol"],
                        price=item["price"],
                        change_24h=item["change_24h"],
                        volume_24h=item["volume_24h"],
                        market_cap=item["market_cap"]
                    )
                    trending.append(coin)
                except KeyError as e:
                    logger.warning(f"Пропущена трендовая монета с отсутствующим полем: {e}")
                    continue
            
            logger.info(f"Получено {len(trending)} трендовых монет")
            return trending
            
        except Exception as e:
            logger.error(f"Ошибка получения трендовых монет: {e}")
            raise ExternalAPIError("CoinMarketCap", 500, str(e))
    
    async def get_historical_data(self, coin_id: str, days: int) -> List[Dict[str, Any]]:
        """
        Получение исторических данных
        """
        try:
            data = await self.client.get_historical_data(coin_id, days)
            logger.info(f"Получено {len(data)} исторических записей для {coin_id}")
            return data
        except Exception as e:
            logger.error(f"Ошибка получения исторических данных для {coin_id}: {e}")
            raise ExternalAPIError("CoinMarketCap", 500, str(e)) 