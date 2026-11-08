import yfinance as yf
from datetime import datetime, timedelta
from utils.logger import setup_logger

logger = setup_logger("CloudClient", "INFO")

class CloudClient:
    def __init__(self):
        # Gold Futures symbol on Yahoo Finance
        self.symbol = "GC=F"
        logger.info("Connected to Yahoo Finance Data Feed.")

    def get_ohlcv(self, timeframe: str = "15m", limit: int = 200) -> list:
        try:
            ticker = yf.Ticker(self.symbol)
            # جلب بيانات آخر 5 أيام لإطار 15 دقيقة
            df = ticker.history(period="5d", interval="15m")
            
            if df.empty:
                raise ValueError("No data returned from Yahoo Finance.")
            
            # تحويل البيانات لشكل يفهمه محركنا
            data = []
            for index, row in df.tail(limit).iterrows():
                data.append({
                    'time': int(index.timestamp() * 1000),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': float(row['Volume']) if row['Volume'] > 0 else 1.0
                })
            return data
        except Exception as e:
            logger.error(f"Failed to fetch Yahoo data: {e}")
            raise
