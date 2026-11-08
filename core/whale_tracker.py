import pandas as pd

class WhaleTracker:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def detect_institutional_candles(self) -> dict:
        self.df['vol_sma'] = self.df['volume'].rolling(window=20).mean()
        last = self.df.iloc[-1]
        
        volume_spike = last['volume'] > (last['vol_sma'] * 2.5)
        body = abs(last['close'] - last['open'])
        total_range = last['high'] - last['low']
        is_strong_body = (body / total_range) > 0.7 if total_range > 0 else False
        
        if volume_spike and is_strong_body:
            direction = "BULLISH" if last['close'] > last['open'] else "BEARISH"
            return {"detected": True, "direction": direction, "message": f"🐋 بصمة حوت {direction} مكتشفة!"}
        
        return {"detected": False, "message": "لا توجد بصمات غير طبيعية."}
