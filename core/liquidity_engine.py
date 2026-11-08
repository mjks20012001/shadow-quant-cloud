import pandas as pd

class LiquidityEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def find_liquidity_pools(self, lookback: int = 50) -> dict:
        recent = self.df.tail(lookback)
        recent_high = recent['high'].max()
        recent_low = recent['low'].min()
        current = self.df['close'].iloc[-1]
        
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
