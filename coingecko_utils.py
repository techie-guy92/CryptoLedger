import aiohttp
import asyncio
import json
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

#====================================== fetch coins price ==============================================

async def get_price(url, session):
    async with session.get(url) as response:
        return await response.json()

async def fetch_coins_prices():
    async with aiohttp.ClientSession() as session:
        urls = {
            "XRP": "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd",
            "ADA": "https://api.coingecko.com/api/v3/simple/price?ids=cardano&vs_currencies=usd",
            "AVAX": "https://api.coingecko.com/api/v3/simple/price?ids=avalanche-2&vs_currencies=usd",
            "LINK": "https://api.coingecko.com/api/v3/simple/price?ids=chainlink&vs_currencies=usd",
            "ENA": "https://api.coingecko.com/api/v3/simple/price?ids=ethena&vs_currencies=usd",
            "PEPE": "https://api.coingecko.com/api/v3/simple/price?ids=pepe&vs_currencies=usd"
        }

        results = {}
        for coin, url in urls.items():
            try:
                raw = await get_price(url, session)
                data = json.loads(raw)
                # Special handling for rate-limit or errors
                if "status" in data:
                    results[coin] = f"Error: {data['status']['error_message']}"
                else:
                    price = list(data.values())[0]["usd"]
                    results[coin] = price
                await asyncio.sleep(1)  
            except Exception as error:
                results[coin] = f"Error: {error}"
        return results


async def main():
    individual = await fetch_coins_prices()
    return individual

# print(asyncio.run(main()))


#====================================== fetch bulk prices ==============================================

SYMBOL_TO_ID = {
    "ETH": "ethereum", "SOL": "solana", "XRP": "ripple", "ADA": "cardano", "AVAX": "avalanche-2", "LINK": "chainlink", 
    "DOT": "polkadot", "AAVE": "aave", "UNI": "uniswap", "AXS": "axie-infinity", "SUSHI": "sushi", "XLM": "stellar",
    "FIL": "filecoin", "NEAR": "near", "EGLD": "elrond-erd-2", "1INCH": "1inch", "SAND": "the-sandbox", "WLD": "worldcoin-wld",
    "ENA": "ethena", "SUI": "sui", "APE": "apecoin", "RENDER": "render-token", "ARB": "arbitrum", "CRV": "curve-dao-token",  
    "WAVES": "waves", "FET": "fetch-ai", "AIOZ": "aioz-network", "GMT": "stepn", "GRT": "the-graph", "CHZ": "chiliz", 
    "GALA": "gala", "ONE": "harmony", "PEPE": "pepe",
}

async def fetch_bulk_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(SYMBOL_TO_ID.values()), "vs_currencies": "usd"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                data = await response.json()
                
                # prices = {symbol: f"{data.get(coin_id, {}).get('usd', 0):.7f}" for symbol, coin_id in SYMBOL_TO_ID.items()}
                prices = {symbol: f"{data.get(coin_id, {}).get('usd', 0):.7f}".rstrip("0").rstrip(".") for symbol, coin_id in SYMBOL_TO_ID.items()}
                
                return {
                    "timestamp": datetime.utcnow().isoformat(), 
                    "prices": prices
                }

        except Exception as error:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "prices": {},
                "error": f"{str(error)} (URL: {url})"
            }


def get_bulk_prices_sync():
    logger.debug(f"Fetched prices successfully at {datetime.utcnow().isoformat()}")
    return asyncio.run(fetch_bulk_prices())


#=======================================================================================================