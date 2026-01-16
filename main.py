import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import Groq

# 1. Initialize App
app = FastAPI()

# 2. Setup Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 3. Define Input Format
# We accept flexible inputs just in case
class ChatRequest(BaseModel):
    message: str

# 4. Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    
    try:
        # Ask Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": user_input}
            ],
            model="llama3-8b-8192",
        )
        
        bot_response = chat_completion.choices[0].message.content
        
        # --- THE FIX ---
        # Send the answer back using ALL common names.
        # This ensures your frontend finds it no matter what it's looking for.
        return {
            "response": bot_response,
            "reply": bot_response,
            "text": bot_response,
            "answer": bot_response,
            "message": bot_response
        }

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg) # Print to logs
        return {
            "response": error_msg,
            "reply": error_msg,
            "text": error_msg,
            "answer": error_msg,
            "message": error_msg
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

