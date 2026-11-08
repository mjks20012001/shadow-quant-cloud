class WhaleTracker:
    def __init__(self, data: list):
        self.data = data

    def detect_institutional_candles(self) -> dict:
        if len(self.data) < 20:
            return {"detected": False, "message": "بيانات غير كافية."}
            
        recent_data = self.data[-20:]
        volumes = [c['volume'] for c in recent_data]
        avg_volume = sum(volumes) / len(volumes)
        
        last = self.data[-1]
        volume_spike = last['volume'] > (avg_volume * 2.5)
        
        body = abs(last['close'] - last['open'])
        total_range = last['high'] - last['low']
        is_strong_body = (body / total_range) > 0.7 if total_range > 0 else False
        
        if volume_spike and is_strong_body:
            direction = "BULLISH" if last['close'] > last['open'] else "BEARISH"
            return {"detected": True, "direction": direction, "message": f"🐋 بصمة حوت {direction} مكتشفة!"}
        
        return {"detected": False, "message": "لا توجد بصمات غير طبيعية."}
