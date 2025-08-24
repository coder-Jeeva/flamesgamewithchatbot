# from fastapi import FastAPI
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# import requests
# import os
# from dotenv import load_dotenv

# # Load .env file
# load_dotenv()

# app = FastAPI()

# # Enable CORS (so frontend JS can call backend without errors)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ⚠️ In production, restrict this to your domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Serve static files (CSS, JS, images)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Secret for Direct Line
# DIRECT_LINE_SECRET = os.getenv("DIRECT_LINE_SECRET", "YOUR_DIRECT_LINE_SECRET")

# @app.get("/api/token")
# def generate_token():
#     """Generate a Direct Line token for Web Chat."""
#     url = "https://directline.botframework.com/v3/directline/tokens/generate"
#     headers = {"Authorization": f"Bearer {DIRECT_LINE_SECRET}"}
#     response = requests.post(url, headers=headers)

#     # Debugging: if secret is wrong, log the response
#     if response.status_code != 200:
#         return {
#             "error": "Token generation failed",
#             "details": response.json()
#         }

#     return response.json()

# @app.get("/")
# def serve_home():
#     """Serve the frontend HTML page."""
#     return FileResponse("index.html")




from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from constant99 import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, CHAT_COMPLETION_NAME
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# # Azure OpenAI
# AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_OPENAI_DEPLOYMENT = os.getenv("CHAT_COMPLETION_NAME")  # deployment name

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2023-07-01-preview"
)

@app.post("/api/chat")
async def chat_with_openai(request: Request):
    body = await request.json()
    user_message = body.get("message")
    if not user_message:
        return {"error": "Missing 'message' in request body"}

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        answer = response.choices[0].message.content
        return {"reply": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def serve_home():
    return FileResponse("index.html")
