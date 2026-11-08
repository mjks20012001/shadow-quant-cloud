from fastapi import FastAPI, WebSocket, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio, json
from core.cloud_client import CloudClient
from core.whale_tracker import WhaleTracker
from core.liquidity_engine import LiquidityEngine
from core.ai_oracle import AIOracle
from utils.logger import setup_logger

logger = setup_logger("WebApp", "INFO")
app = FastAPI()
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

client = CloudClient()
ai_oracle = AIOracle()

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze_chart")
async def analyze_chart(file: UploadFile = File(...)):
    contents = await file.read()
    result = ai_oracle.analyze_market_vision(contents)
    return JSONResponse(content={"analysis": result})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            df = client.get_ohlcv()
            whale = WhaleTracker(df).detect_institutional_candles()
            liquidity = LiquidityEngine(df).find_liquidity_pools()
            
            payload = {"whale": whale, "liquidity": liquidity}
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(5)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()
