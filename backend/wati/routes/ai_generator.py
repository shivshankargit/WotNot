from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services import ai_service

router = APIRouter(tags=["AI Generator"])

class GreetingRequest(BaseModel):
    user_name: str
    prompt: str

@router.post("/generate-greeting")
async def generate_greeting(request: GreetingRequest):
    greeting = await ai_service.generate_diwali_greeting(request.user_name, request.prompt)
    
    if "Error" in greeting:
        raise HTTPException(status_code=500, detail=greeting)
    
    return {"greeting": greeting}
