import os
import base64
from openai import OpenAI

class AIOracle:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key and api_key != "sk-proj-xxxxxxxxxxxxxxxxxxxx" else None

    def analyze_market_vision(self, image_bytes: bytes) -> str:
        if not self.client:
            return "❌ مفتاح OpenAI غير موجود أو غير صحيح. يرجى إضافته في إعدادات Render."
            
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "حلل هذا الشارت للذهب. اذكر الاتجاه، مناطق السيولة (Liquidity Sweeps)، ومناطق العرض والطلب (Order Blocks) باختصار شديد."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ خطأ في التحليل: {str(e)}"
