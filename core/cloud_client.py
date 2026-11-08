import ccxt
from utils.logger import setup_logger

logger = setup_logger("CloudClient", "INFO")

class CloudClient:
    def __init__(self):
        self.exchange = ccxt.binance()
        logger.info("Connected to Binance Data Feed.")

    def get_ohlcv(self, symbol: str = "XAUUSDT", timeframe: str = "15m", limit: int = 200) -> list:
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            # تحويل البيانات إلى قائمة من القواميس بدل DataFrame
            data = []
            for candle in ohlcv:
                data.append({
                    'time': candle[0],
                    'open': candle[1],
                    'high': candle[2],
                    'low': candle[3],
                    'close': candle[4],
                    'volume': candle[5]
                })
            return data
        except Exception as e:
            logger.error(f"Failed to fetch Binance data: {e}")
            raise
