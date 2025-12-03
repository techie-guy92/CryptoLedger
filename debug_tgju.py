import sys
import os
import django
import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Setup Django
sys.path.append('/app') 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

async def debug_fetch():
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
                missing = [k for k, sel in selectors.items() if not soup.select_one(sel)]
                raise ValueError(f"Missing elements: {', '.join(missing)}")

            usd_raw = usd_element.text.strip().replace(",", "").replace(".", "")
            usdt_raw  = usdt_element.text.strip().replace(",", "").replace(".", "")
            
            usd_price = int(usd_raw[:-1] if usd_raw.endswith("0") else usd_raw)
            usdt_price = int(usdt_raw[:-1] if usdt_raw.endswith("0") else usdt_raw)
            ounce_price = round(float(ounce_element.text.strip().replace(",", "")), 2)

            prices = {
                "USD": f"{usd_price:,.0f}",
                "USDT": f"{usdt_price:,.0f}",
                "OUNCE": f"{ounce_price:,.2f}"
            }
            
            print("DEBUG INFO:")
            print(f"USD Raw: {usd_raw}")
            print(f"USD Price: {usd_price}")
            print(f"USDT Raw: {usdt_raw}")
            print(f"USDT Price: {usdt_price}")
            print(f"Ounce Price: {ounce_price}")
            print(f"All Prices: {prices}")
            
            return {
                "usd_raw": usd_raw,
                "usd_price": usd_price,
                "prices": prices
            }

        except Exception as error:
            print(f"Error: {error}")
            import traceback
            # Show full error trace
            traceback.print_exc()  
            return None

if __name__ == "__main__":
    print("Starting TGJU debug fetch...")
    result = asyncio.run(debug_fetch())
    print("\n" + "="*50)
    print("FINAL RESULT:")
    print("="*50)
    print(result)