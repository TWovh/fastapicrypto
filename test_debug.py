import httpx

COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

async def test_url():
    url = f"{COINGECKO_API_BASE}/coins/markets"
    print(f"Testing URL: {url}")
    
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, params={"vs_currency": "usd", "per_page": 1})
            print(f"Status: {response.status_code}")
            print(f"Success!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_url()) 