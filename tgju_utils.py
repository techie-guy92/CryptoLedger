import aiohttp
import asyncio
import json
import logging
from bs4 import BeautifulSoup
from datetime import datetime


logger = logging.getLogger(__name__)

#====================================== fetch usd & ounce prices ======================================

async def fetch_usd_and_ounce_prices():
    url = "https://www.tgju.org/"
    selectors = {
        "usd": "#l-price_dollar_rl .info-price",
        "usdt": "#l-crypto-tether-irr .info-price",
        "ounce": "#l-ons .info-price"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                html = await response.text()

            soup = BeautifulSoup(html, "lxml")
            usd_element = soup.select_one(selectors["usd"])
            usdt_element = soup.select_one(selectors["usdt"])
            ounce_element = soup.select_one(selectors["ounce"])

            if not usd_element or not usdt_element or not ounce_element:
                raise ValueError("Required elements not found in response.")

            usd_raw = usd_element.text.strip().replace(",", "").replace(".", "")
            usdt_raw  = usdt_element.text.strip().replace(",", "").replace(".", "")
            
            usd_price = int(usd_raw[:-1] if usd_raw.endswith("0") else usd_raw)
            usdt_price = int(usdt_raw[:-1] if usdt_raw.endswith("0") else usdt_raw)
            ounce_price = round(float(ounce_element.text.strip().replace(",", "")), 2)

            prices = {
                "USD": usd_price,
                "USDT": usdt_price,
                "OUNCE": ounce_price
            }

            logger.debug(f"Fetched USD/IRT: {usd_price}, Ounce: {ounce_price}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "prices": prices
            }

        except Exception as error:
            logger.error(f"Failed to fetch USD/Ounce prices: {error}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "prices": {},
                "error": str(error)
            }

def get_usd_and_ounce_prices_sync():
    logger.debug(f"Fetching USD & Ounce prices at {datetime.utcnow().isoformat()}")
    return asyncio.run(fetch_usd_and_ounce_prices())


#=======================================================================================================                     