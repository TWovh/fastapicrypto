import httpx
import asyncio

async def test_coingecko_api():
    """Тестируем API CoinGecko"""
    async with httpx.AsyncClient() as client:
        # Тест 1: /search/trending
        print("Тестируем /search/trending...")
        try:
            response = await client.get("https://api.coingecko.com/api/v3/search/trending")
            print(f"Статус: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Данные: {data.keys()}")
            else:
                print(f"Ошибка: {response.text}")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Тест 2: /coins/markets (альтернативный метод)
        print("Тестируем /coins/markets...")
        try:
            response = await client.get("https://api.coingecko.com/api/v3/coins/markets", params={
                "vs_currency": "usd",
                "order": "price_change_percentage_24h_desc",
                "per_page": 5,
                "page": 1,
                "sparkline": False
            })
            print(f"Статус: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Получено монет: {len(data)}")
                for coin in data[:3]:
                    print(f"- {coin['name']} ({coin['symbol']}): ${coin['current_price']}")
            else:
                print(f"Ошибка: {response.text}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_coingecko_api()) 