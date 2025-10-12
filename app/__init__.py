from pathlib import Path
from fastapi import FastAPI
from app.http.routes.post import router as file_post_router
from app.http.routes.get import router as file_get_router
from fastapi.middleware.cors import CORSMiddleware


app = None

def create_app():
    global app

    #app init
    app = FastAPI(
        title="Loader Service API",
        version="1.0.0",
    )

    #init
    init_client()
    #register
    app.include_router(file_post_router)
    app.include_router(file_get_router)
    #command init

    return app

__all__ = ['app', 'create_app']

def init_client():
    pass
#config
#client

