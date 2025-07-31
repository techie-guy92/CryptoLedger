from tradingview_ta import TA_Handler, Interval, Exchange
import asyncio
import aiohttp
 

# pip install -U tradingview_ta
#====================================== fetch Coins Data ==============================================

class Interval:
    INTERVAL_1_MINUTE = "1m"
    INTERVAL_5_MINUTES = "5m"
    INTERVAL_15_MINUTES = "15m"
    INTERVAL_30_MINUTES = "30m"
    INTERVAL_1_HOUR = "1h"
    INTERVAL_2_HOURS = "2h"
    INTERVAL_4_HOURS = "4h"
    INTERVAL_1_DAY = "1d"
    INTERVAL_1_WEEK = "1W"
    INTERVAL_1_MONTH = "1M"


def fetchCoinsData(timeframe):
    
    # symbols = [
    #     "BINANCE:BTCUSDT-BTCUSDT"  , "BINANCE:ETHUSDT-ETHUSDT"    , "BINANCE:BNBUSDT-BNBUSDT"    , "BINANCE:SOLUSDT-SOLUSDT"    , "BINANCE:XRPUSDT-XRPUSDT"  , 
    #     "BINANCE:ADAUSDT-ADAUSDT"  , "BINANCE:ATOMUSDT-ATOMUSDT"  , "BINANCE:DOTUSDT-DOTUSDT"    , "BINANCE:LINKUSDT-LINKUSDT"  , "BINANCE:UNIUSDT-UNIUSDT"  , 
    #     "BINANCE:AVAXUSDT-AVAXUSDT", "BINANCE:AAVEUSDT-AAVEUSDT"  , "BINANCE:LTCUSDT-LTCUSDT"    , "BINANCE:NEARUSDT-NEARUSDT"  , 
    #     "BINANCE:XLMUSDT-XLMUSDT"  , "BINANCE:1INCHUSDT-1INCHUSDT", "BINANCE:APTUSDT-APTUSDT"    , "BINANCE:FILUSDT-FILUSDT"    , "BINANCE:AXSUSDT-AXSUSDT"  ,
    #     "BINANCE:SANDUSDT-SANDUSDT", "BINANCE:CAKEUSDT-CAKEUSDT"  , "BINANCE:SUSHIUSDT-SUSHIUSDT", "BINANCE:APEUSDT-APEUSDT"    , "BINANCE:CRVUSDT-CRVUSDT"  ,
    #     "BINANCE:EGLDUSDT-EGLDUSDT", "BINANCE:TONUSDT.P-TONUSDT"  , "BINANCE:RNDRUSDT-RNDRUSDT"  , "BINANCE:ARBUSDT-ARBUSDT"    , "BINANCE:SUIUSDT-SUIUSDT"  ,
    #     "BINANCE:OPUSDT-OPUSDT"    , "BINANCE:WLDUSDT-WLDUSDT"    , "BINANCE:ENAUSDT-ENAUSDT"    ,  "BINANCE:FETUSDT-FETUSDT"   , "BINANCE:GMTUSDT-GMTUSDT"  ,
    #     "BINANCE:DOGEUSDT-DOGEUSDT", "BINANCE:CHZUSDT.P-CHZUSDT"  , "BINANCE:GRTUSDT-GRTUSDT"    , "BINANCE:GALAUSDT-GALAUSDT"  , "BINANCE:ONEUSDT-ONEUSDT"  , 
    #     "BINANCE:SHIBUSDT-SHIBUSDT", "BINANCE:FLOKIUSDT-FLOKIUSDT", "BINANCE:PEPEUSDT-PEPEUSDT"  , "KUCOIN:AIOZUSDT-AIOZUSDT",
    # ]
    
    symbols = [
        "BINANCE:BTCUSDT-BTCUSDT", "BINANCE:ETHUSDT-ETHUSDT", "BINANCE:BNBUSDT-BNBUSDT", "BINANCE:SOLUSDT-SOLUSDT", "BINANCE:XRPUSDT-XRPUSDT",
        "BINANCE:AVAXUSDT-AVAXUSDT", "BINANCE:NEARUSDT-NEARUSDT", "BINANCE:LTCUSDT-LTCUSDT", "BINANCE:TONUSDT.P-TONUSDT", 
        "BINANCE:CAKEUSDT-CAKEUSDT", "BINANCE:SUSHIUSDT-SUSHIUSDT", "BINANCE:AXSUSDT-AXSUSDT", "BINANCE:APEUSDT-APEUSDT", "BINANCE:SUIUSDT-SUIUSDT", 
        "BINANCE:ARBUSDT-ARBUSDT", "BINANCE:SANDUSDT-SANDUSDT", "BINANCE:OPUSDT-OPUSDT", "BINANCE:CHZUSDT.P-CHZUSDT", "BINANCE:DOGEUSDT-DOGEUSDT",
        "BINANCE:GMTUSDT-GMTUSDT", "BINANCE:FLOKIUSDT-FLOKIUSDT", "BINANCE:SHIBUSDT-SHIBUSDT", "BINANCE:PEPEUSDT-PEPEUSDT", "BINANCE:ADAUSDT-ADAUSDT",
        "BINANCE:DOTUSDT-DOTUSDT", "BINANCE:LINKUSDT-LINKUSDT", "BINANCE:UNIUSDT-UNIUSDT", "BINANCE:FILUSDT-FILUSDT", "BINANCE:WLDUSDT-WLDUSDT",
        "BINANCE:APTUSDT-APTUSDT", "BINANCE:ATOMUSDT-ATOMUSDT", "BINANCE:XMRUSDT.P-XMRUSDT", 
        ]
         
    coins = []
    prices = []

    for symbol in symbols:
        exchange, pair = symbol.split(":")
        pair, coin = pair.split("-")
        handler = TA_Handler(
            symbol=pair,
            exchange=exchange,
            screener="crypto",
            interval=timeframe,
            timeout=None,
        )

        analysis_data = handler.get_analysis()

        if analysis_data:
            indicators = analysis_data.indicators
            if indicators:
                open_price = indicators.get("open")
                if open_price:
                    coins.append(coin)
                    prices.append(open_price)
                else:
                    print(f"No open price data available for {coin}")
            else:
                print(f"No indicator data available for {coin}")
        else:
            print(f"No analysis data available for {coin}")

    return coins, prices


#======================================================================================================

timeframe = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1W", "1M"]
coin_list, price_list = fetchCoinsData(timeframe[0])
print(coin_list)
print(price_list)