import os
import requests
from utils.logger import setup_logger

logger = setup_logger("CloudClient", "INFO")

class CloudClient:
    def __init__(self):
        self.api_key = os.getenv("TWELVEDATA_API_KEY")
        self.symbol = "XAU/USD"
        logger.info("Connected to TwelveData Feed.")

    def get_ohlcv(self, timeframe: str = "15min", limit: int = 200) -> list:
        try:
            url = f"https://api.twelvedata.com/time_series?symbol={self.symbol}&interval={timeframe}&outputsize={limit}&apikey={self.api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            res_data = response.json()
            
            if "values" not in res_data:
                raise ValueError(f"TwelveData Error: {res_data.get('message', 'Unknown')}")

            data = []
            # TwelveData returns newest first, we reverse to oldest first
            for item in reversed(res_data["values"]):
                data.append({
                    'time': item['datetime'],
                    'open': float(item['open']),
                    'high': float(item['high']),
                    'low': float(item['low']),
                    'close': float(item['close']),
                    'volume': float(item['volume']) if item['volume'] else 1.0
                })
            return data
        except Exception as e:
            logger.error(f"Failed to fetch TwelveData: {e}")
            raise
