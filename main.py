from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

# Enable CORS (so frontend JS can call backend without errors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Secret for Direct Line
DIRECT_LINE_SECRET = os.getenv("DIRECT_LINE_SECRET", "YOUR_DIRECT_LINE_SECRET")

@app.get("/api/token")
def generate_token():
    """Generate a Direct Line token for Web Chat."""
    url = "https://directline.botframework.com/v3/directline/tokens/generate"
    headers = {"Authorization": f"Bearer {DIRECT_LINE_SECRET}"}
    response = requests.post(url, headers=headers)

    # Debugging: if secret is wrong, log the response
    if response.status_code != 200:
        return {
            "error": "Token generation failed",
            "details": response.json()
        }

    return response.json()

@app.get("/")
def serve_home():
    """Serve the frontend HTML page."""
    return FileResponse("index.html")