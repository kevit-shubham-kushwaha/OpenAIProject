from fastapi import FastAPI
import uvicorn

from libs.utils.middleware.request_data import RequestDataMiddleware
from libs.utils.config import config
from src import logger

app = FastAPI()

logger.info("Starting FastAPI application...")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.add_middleware(RequestDataMiddleware)

if __name__ == "__main__":
    if config.HOST is None or config.PORT is None:
        logger.error("HOST or PORT is not set in the configuration.")
        raise ValueError("HOST or PORT is not set in the configuration.")
    
    uvicorn.run(app, host=config.HOST, port=int(config.PORT))
