from fastapi import FastAPI
from fastapi import HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI()

BARK_URL = "https://api.bark.com/process"





class PromptRequest(BaseModel):
    prompt: str

@app.post("/process-prompt")
async def process_prompt(request: PromptRequest):
    prompt = request.prompt
    if len(prompt) < 10:
        raise HTTPException(status_code=400, detail="Prompt must be at least 10 characters long.")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(BARK_URL, json={"prompt": prompt})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=500, detail="Error processing prompt")


