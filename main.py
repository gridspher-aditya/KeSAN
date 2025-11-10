# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import requests
from agent.apple_orchard_agent import invoke_agent
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Apple Orchard AI Agent API",
    description="AI-powered advisory system for apple orchard management",
    version="1.0.0"
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
#                         REQUEST MODELS
# ═══════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    device_id: str = Field(..., description="Farm device ID")
    message: str = Field(..., description="Farmer's question or request")
    conversation_id: Optional[str] = Field(None, description="Session ID for conversation tracking")

class ChatResponse(BaseModel):
    response: str
    advisor_used: str
    sensor_data_used: bool
    conversation_id: str
    device_id: str

class SensorDataResponse(BaseModel):
    device_id: str
    readings: List[dict]
    total_readings: int

# ═══════════════════════════════════════════════════════════════
#                           ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def simple_html_response():
    # Define your simple HTML content as a string
    html_content = """
    <html>
        <body>
            <h1>Hello, UpTimeRobot!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Main chat endpoint for farmers to interact with AI advisors
    """
    try:
        # Validate device_id
        if not request.device_id or not request.device_id.strip():
            raise HTTPException(status_code=400, detail="Device ID is required")
        
        # Invoke the LangGraph agent
        result = invoke_agent(
            device_id=request.device_id,
            message=request.message
        )
        
        return ChatResponse(
            response=result["response"],
            advisor_used=result["advisor_used"],
            sensor_data_used=result["sensor_data_used"],
            conversation_id=request.conversation_id or "new_session",
            device_id=request.device_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/api/sensor-data/{device_id}", response_model=SensorDataResponse)
async def get_sensor_data(device_id: str, limit: int = 10):
    """
    Fetch raw sensor data for dashboard visualization
    """
    try:
        url = f"https://gridsphere.in/dapi/?d_id={device_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        readings = data.get("readings", [])
        
        return SensorDataResponse(
            device_id=device_id,
            readings=readings[:limit],
            total_readings=len(readings)
        )
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sensor data: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api_connection": "active",
        "anthropic_api": "configured" if os.getenv("ANTHROPIC_API_KEY") else "missing"
    }

# ═══════════════════════════════════════════════════════════════
#                         RUN THE APP
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
