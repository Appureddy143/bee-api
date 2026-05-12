from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
import google.generativeai as genai
import os

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Use gemini-1.5-flash which is standard and fast
model = genai.GenerativeModel('gemini-1.5-flash')

@router.post("/chat", response_model=schemas.AiChatResponse)
def chat_with_ai(request: schemas.AiChatRequest, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not GEMINI_API_KEY:
        return {"response": "AI Assistant is currently unavailable (Missing API Key). Please consult an agricultural expert."}

    prompt = f"You are an agricultural AI assistant helping a {current_user.role}. Answer the following query concisely: {request.prompt}"
    
    try:
        response = model.generate_content(prompt)
        ai_response_text = response.text
        
        chat_log = models.AiChatHistory(
            user_id=current_user.id,
            prompt=request.prompt,
            response=ai_response_text
        )
        db.add(chat_log)
        db.commit()
        
        return {"response": ai_response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
