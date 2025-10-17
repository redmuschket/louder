from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as auth_rout


app = None

def create_app():
    global app

    #app init
    app = FastAPI(
        title="Auth Service API",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    #init
    init_client()
    #register
    app.include_router(auth_rout)
    #command init

    return app

__all__ = ['app', 'create_app']

def init_client():
    pass
