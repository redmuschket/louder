import os
import uvicorn
from app import create_app
from dotenv import load_dotenv

app = create_app()

if __name__ == "__main__":
    load_dotenv()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8011))
    uvicorn.run("main:app", host=host, port=port, reload=True)