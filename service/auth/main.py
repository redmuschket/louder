import uvicorn
from app import create_app
import asyncio
import asyncpg
import os

app = create_app()
