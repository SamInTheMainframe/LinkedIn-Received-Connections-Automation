from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .linkedin_bot import LinkedInBot
from .scoring import ConnectionScorer

app = FastAPI()
bot = LinkedInBot('cookies.json')
scorer = ConnectionScorer()

class Connection(BaseModel):
    name: str
    title: str
    profile_url: str
    message: str
    score: int = 0

@app.get("/connections/", response_model=List[Connection])
async def get_connections():
    connections = bot.get_pending_connections()
    
    # Score each connection
    for connection in connections:
        connection['score'] = scorer.calculate_score(connection)
    
    return connections

@app.post("/connections/{profile_url}/accept")
async def accept_connection(profile_url: str):
    try:
        bot.accept_connection(profile_url)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/connections/{profile_url}/message")
async def send_message(profile_url: str, message: str):
    try:
        bot.send_message(profile_url, message)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 