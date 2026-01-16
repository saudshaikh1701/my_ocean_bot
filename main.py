import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import Groq

# 1. Initialize the App
app = FastAPI()

# 2. Setup the "Groq" Brain
# It looks for the key in your Render Environment Variables
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Define the data format for incoming messages
class ChatRequest(BaseModel):
    message: str

# 3. Mount the Static Folder 
# (This serves your CSS, Images, and Javascript)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. The Home Route (Loads your Website)
@app.get("/")
async def read_root():
    # This assumes your index.html is inside the 'static' folder.
    # If your index.html is in a 'templates' folder, change this line!
    return FileResponse('static/index.html')

# 5. The Chat Route (Where the magic happens)
@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    
    try:
        # Ask Groq (Llama 3) for an answer
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-8b-8192", # This is the free, fast model
        )
        
        # Extract the answer
        bot_response = chat_completion.choices[0].message.content
        
        return {"response": bot_response}

    except Exception as e:
        # If something breaks, tell the user
        return {"response": f"Error: {str(e)}"}

# 6. Run the Server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)