import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# 1. Setup Groq (The Brain)
# It will look for the key in Render's settings
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class ChatRequest(BaseModel):
    message: str

# 2. Serve the Website files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Ask Groq (Llama 3)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": request.message}
            ],
            model="llama3-8b-8192",
        )
        
        # Get the answer
        bot_reply = chat_completion.choices[0].message.content
        
        # Send it back in a format our new website expects
        return {"reply": bot_reply}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

