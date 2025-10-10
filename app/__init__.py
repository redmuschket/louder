from pathlib import Path
from fastapi import FastAPI
from app.http.routes.patent import router as patent_router
from app.http.routes.get import router as analog_get_router
from app.http.routes.creat import router as analog_create_route
from app.http.routes.table import router as analog_table_route
from app.clients.parser_client import ParserClient
from app.clients.client_llm_client import LLMClientClient
from app.clients.user_client import UserClient
from core.manager_config.service_client.llm_client import LLMClientServiceManagerConfig
from core.manager_config.service_client.user import UserServiceManagerConfig
from core.manager_config.service_client.parser import ParserServiceManagerConfig
from fastapi.middleware.cors import CORSMiddleware
from app.http.routes.web_socket import router as ws_router
app = None

def create_app():
    global app

    #app init
    app = FastAPI(
        title="Patent Service API",
        version="1.0.0",
    )

    #init
    init_client()
    #register
    app.include_router(patent_router)
    app.include_router(analog_get_router)
    app.include_router(analog_create_route)
    app.include_router(analog_table_route)
    app.include_router(ws_router)
    #command init

    return app

__all__ = ['app', 'create_app']

def init_client():
    #config
    llm_config = LLMClientServiceManagerConfig()
    user_config = UserServiceManagerConfig()
    parser_config = ParserServiceManagerConfig()
    #client
    LLMClientClient(llm_config)
    UserClient(user_config)
    ParserClient(parser_config)