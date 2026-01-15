from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load Keys
load_dotenv()
# We use os.getenv to safely get the key from your .env file
# Make sure your .env file has OPENAI_API_KEY or GOOGLE_API_KEY
# But for now, we will paste the key here to be safe:
MY_KEY = "AIzaSyAhYExFlRSfJrylLEUkeUipySLs6ZnyyUA"
genai.configure(api_key=MY_KEY)

# 2. Setup Model (Use the one that worked for you!)
# Update this line to give it a specific job
model = genai.GenerativeModel(
    'models/gemini-2.5-flash', # Keep YOUR working model name here!
    system_instruction="You are a sarcastic robot from the year 3000. You make fun of humans gently."
) 
chat_session = model.start_chat(history=[])

app = FastAPI()

# 3. Allow Connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. The Chat Logic
@app.post("/chat")
async def chat(message: str):
    try:
        response = chat_session.send_message(message)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

# 5. Serve the Website (The Magic Part)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

