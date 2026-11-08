import os
import base64
from groq import Groq

class AIOracle:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key) if api_key and api_key != "none" else None

    def analyze_market_vision(self, image_bytes: bytes) -> str:
        if not self.client:
            return "❌ مفتاح Groq غير موجود. يرجى إضافته في إعدادات Render."
            
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        try:
            # استخدام نموذج الرؤية المجاني من Groq
            response = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "حلل هذا الشارت للذهب. اذكر الاتجاه، مناطق السيولة (Liquidity Sweeps)، ومناطق العرض والطلب (Order Blocks) باختصار شديد."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ خطأ في التحليل: {str(e)}"
