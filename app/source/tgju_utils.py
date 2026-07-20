import asyncio
import json
import logging
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ====================================== fetch usd & ounce prices ======================================


async def fetch_usd_and_ounce_prices():
    url = "https://www.tgju.org/"
    selectors = {
        "usd": "#l-price_dollar_rl .info-price",
        "usdt": "#l-crypto-tether-irr .info-price",
        "ounce": "#l-ons .info-price",
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                html = await response.text()

            soup = BeautifulSoup(html, "lxml")
            usd_element = soup.select_one(selectors["usd"])
            usdt_element = soup.select_one(selectors["usdt"])
            ounce_element = soup.select_one(selectors["ounce"])

            if not usd_element or not usdt_element or not ounce_element:
                missing = [
                    k for k, sel in selectors.items() if not soup.select_one(sel)
                ]
                raise ValueError(f"Missing elements: {", ".join(missing)}")

            usd_raw = usd_element.text.strip().replace(",", "").replace(".", "")
            usdt_raw = usdt_element.text.strip().replace(",", "").replace(".", "")

            usd_price = int(usd_raw[:-1] if usd_raw.endswith("0") else usd_raw)
            usdt_price = int(usdt_raw[:-1] if usdt_raw.endswith("0") else usdt_raw)
            ounce_price = round(float(ounce_element.text.strip().replace(",", "")), 2)

            prices = {
                "USD": f"{usd_price:,.0f}",
                "USDT": f"{usdt_price:,.0f}",
                "OUNCE": f"{ounce_price:,.2f}",
            }

            logger.debug(f"Fetched USD/USDT/IRT: {usd_price}, Ounce: {ounce_price}")
            return {"timestamp": datetime.utcnow().isoformat(), "prices": prices}

        except Exception as error:
            logger.error(f"Failed to fetch USD/USDT/Ounce prices: {error}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "prices": {},
                "error": repr(error),
            }


def get_usd_and_ounce_prices_sync():
    logger.debug(
        f"Fetching USD & USDT & Ounce prices at {datetime.utcnow().isoformat()}"
    )
    return asyncio.run(fetch_usd_and_ounce_prices())


# =======================================================================================================
