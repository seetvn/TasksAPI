from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

#TODO: hide key in environment variable or config file
API_KEY = os.environ["API_KEY"]

async def api_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/auth/") or request.url.path.startswith("/tasks/"):
        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return JSONResponse(status_code=401, content={"detail": "Invalid or missing API key"})
    return await call_next(request)
