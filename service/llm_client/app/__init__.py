from fastapi import FastAPI
from app.http.routes.routes import router as main_routes
from app.http.routes.web_socket import router as web_socket_router

app = None

def create_app():
    global app

    # app init
    app = FastAPI(
        title="LLM Client Service API",
        version="1.0.0",
    )

    #register
    app.include_router(main_routes)
    app.include_router(web_socket_router)

    return app

__all__ = ['app', 'create_app']