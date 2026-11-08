import ccxt
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger("CloudClient", "INFO")

class CloudClient:
    def __init__(self):
        self.exchange = ccxt.binance()
        logger.info("Connected to Binance Data Feed.")

    def get_ohlcv(self, symbol: str = "XAUUSDT", timeframe: str = "15m", limit: int = 200) -> pd.DataFrame:
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"Failed to fetch Binance data: {e}")
            raise
