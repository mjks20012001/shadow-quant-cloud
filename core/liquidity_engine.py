class LiquidityEngine:
    def __init__(self, data: list):
        self.data = data

    def find_liquidity_pools(self, lookback: int = 50) -> dict:
        if len(self.data) < lookback:
            return {"warning": "SAFE", "message": "بيانات غير كافية.", "high": 0, "low": 0}
            
        recent = self.data[-lookback:]
        recent_high = max(c['high'] for c in recent)
        recent_low = min(c['low'] for c in recent)
        current = self.data[-1]['close']
        
        dist_high = abs(current - recent_high)
        dist_low = abs(current - recent_low)
        
        warning = "SAFE"
        msg = "السيولة بعيدة، حركة السعر طبيعية."
        
        if dist_high < (current * 0.002):
            warning = "HIGH_LIQUIDITY_ABOVE"
            msg = "⚠️ السعر قريب من سيولة عالية بالأعلى (احتمال Stop Hunt)."
        elif dist_low < (current * 0.002):
            warning = "HIGH_LIQUIDITY_BELOW"
            msg = "⚠️ السعر قريب من سيولة عالية بالأسفل (احتمال Stop Hunt)."
            
        return {"warning": warning, "message": msg, "high": round(recent_high, 2), "low": round(recent_low, 2)}
