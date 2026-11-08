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
            response = self.client.chat.completions.create(
                model="llama-3.2-90b-vision-preview", # موديل محدث
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "أنت خبير تداول. حلل هذا الشارت بالعربية. اذكر الاتجاه، مناطق السيولة (Liquidity)، ومناطق العرض والطلب (Order Blocks) باختصار."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }],
                max_tokens=600
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ خطأ في التحليل: {str(e)}"
