import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# 1. Setup Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 2. Initialize Memory (The History List)
# We start with a "System Message" to give the bot a personality
chat_history = [
    {"role": "system", "content": "You are a helpful and friendly AI assistant named Cerulean."}
]

class ChatRequest(BaseModel):
    message: str

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/chat")
async def chat(request: ChatRequest):
    global chat_history
    
    try:
        # A. Add the User's new message to history
        chat_history.append({"role": "user", "content": request.message})
        
        # B. Send the WHOLE history to Groq (so it remembers)
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="llama-3.1-8b-instant", # The fast, new model
        )
        
        # C. Get the answer
        bot_reply = chat_completion.choices[0].message.content
        
        # D. Add the Bot's answer to history
        chat_history.append({"role": "assistant", "content": bot_reply})
        
        return {"reply": bot_reply}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

