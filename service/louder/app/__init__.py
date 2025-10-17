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

    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # откуда можно слать запросы
        allow_credentials=True,
        allow_methods=["*"],  # разрешаем все методы (GET, POST, PUT, DELETE)
        allow_headers=["*"],  # разрешаем любые заголовки, включая X-User-Id
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

